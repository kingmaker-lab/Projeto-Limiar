package atlas

import (
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"encoding/hex"
	"strings"
	"sync"
	"testing"
)

func testWallet(t testing.TB) (*ecdsa.PrivateKey, string) {
	t.Helper()
	key, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	address, err := Address(&key.PublicKey)
	if err != nil {
		t.Fatal(err)
	}
	return key, address
}

func testLedger(t *testing.T, miner string) *Ledger {
	t.Helper()
	ledger, err := NewLedger()
	if err != nil {
		t.Fatal(err)
	}
	if _, err := ledger.Mine(miner, nil); err != nil {
		t.Fatal(err)
	}
	return ledger
}

func testSign(t testing.TB, network string, key *ecdsa.PrivateKey, to string, amount, nonce uint64) *Transaction {
	t.Helper()
	tx, err := Sign(network, key, to, amount, nonce)
	if err != nil {
		t.Fatal(err)
	}
	return tx
}

func TestTransfers(t *testing.T) {
	key, alice := testWallet(t)
	_, bob := testWallet(t)
	otherKey, _ := testWallet(t)
	ledger := testLedger(t, alice)
	tx := testSign(t, ledger.Network, key, bob, 17, 1)
	conflict := testSign(t, ledger.Network, key, bob, 18, 1)
	wrongKey := testSign(t, ledger.Network, otherKey, bob, 17, 1)
	wrongKey.From = alice
	tampered := *tx
	tampered.Amount = 19

	for _, tc := range []struct {
		name string
		tx   *Transaction
		want string
	}{
		{"adulterada", &tampered, "assinatura inválida"},
		{"chave alheia", wrongKey, "chave pública não corresponde"},
		{"saldo insuficiente", testSign(t, ledger.Network, key, bob, 51, 1), "saldo insuficiente"},
		{"nonce futuro", testSign(t, ledger.Network, key, bob, 1, 2), "nonce incorreto"},
		{"outra rede", testSign(t, strings.Repeat("b", 64), key, bob, 17, 1), "assinatura inválida"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			if _, err := ledger.Mine(bob, tc.tx); err == nil || !strings.Contains(err.Error(), tc.want) || len(ledger.Blocks) != 1 {
				t.Fatalf("blocos=%d erro=%v", len(ledger.Blocks), err)
			}
		})
	}
	block, err := ledger.Mine(bob, tx)
	if err != nil {
		t.Fatal(err)
	}
	for _, duplicate := range []*Transaction{tx, conflict} {
		if _, err := ledger.Mine(bob, duplicate); err == nil || !strings.Contains(err.Error(), "nonce incorreto") {
			t.Fatalf("gasto duplo aceito: %v", err)
		}
	}
	block.Transfer.Signature[0] ^= 1
	tx.PublicKey[0] ^= 1
	state, err := ledger.Audit()
	if err != nil {
		t.Fatal(err)
	}
	if state.Supply != 100 || state.Accounts[alice] != (Account{33, 1}) || state.Accounts[bob] != (Account{67, 0}) {
		t.Fatalf("estado inesperado: %+v", state)
	}
}

func TestAuditRejectsInvalidChain(t *testing.T) {
	_, miner := testWallet(t)
	for _, tc := range []struct {
		name   string
		mutate func(*Ledger)
	}{
		{"versão", func(l *Ledger) { l.Version = "other" }},
		{"vínculo", func(l *Ledger) { l.Blocks[0].Previous = strings.Repeat("0", 64) }},
		{"altura", func(l *Ledger) { l.Blocks[0].Height++ }},
		{"trabalho", func(l *Ledger) {
			block := &l.Blocks[0]
			for {
				block.Nonce++
				sum := block.digest(l.Network)
				if sum[0] != 0 {
					block.Hash = hex.EncodeToString(sum[:])
					return
				}
			}
		}},
		{"limite", func(l *Ledger) { l.Blocks = make([]Block, MaxBlocks+1) }},
	} {
		t.Run(tc.name, func(t *testing.T) {
			ledger := testLedger(t, miner)
			tc.mutate(ledger)
			if _, err := ledger.Audit(); err == nil {
				t.Fatal("cadeia inválida aceita")
			}
		})
	}
}

func TestConcurrentWriters(t *testing.T) {
	key, alice := testWallet(t)
	_, bob := testWallet(t)
	ledger := testLedger(t, alice)
	dir := t.TempDir()
	if err := Update(dir, func(_ *Ledger) (*Ledger, error) { return ledger, nil }); err != nil {
		t.Fatal(err)
	}
	var wg sync.WaitGroup
	results := make(chan error, 2)
	for _, amount := range []uint64{17, 18} {
		tx := testSign(t, ledger.Network, key, bob, amount, 1)
		wg.Add(1)
		go func() {
			defer wg.Done()
			results <- Update(dir, func(l *Ledger) (*Ledger, error) {
				_, err := l.Mine(bob, tx)
				return l, err
			})
		}()
	}
	wg.Wait()
	close(results)
	success := 0
	for err := range results {
		if err == nil {
			success++
		} else if !strings.Contains(err.Error(), "nonce incorreto") {
			t.Fatal(err)
		}
	}
	reopened, err := Load(dir)
	if err != nil {
		t.Fatal(err)
	}
	state, err := reopened.Audit()
	if err != nil {
		t.Fatal(err)
	}
	if success != 1 || state.Height != 2 || state.Supply != 100 || state.Accounts[alice].Nonce != 1 {
		t.Fatalf("sucessos=%d estado=%+v", success, state)
	}
}

func BenchmarkAudit1024(b *testing.B) {
	ledger := &Ledger{Version: Version, Network: strings.Repeat("a", 64), Blocks: []Block{}}
	aliceKey, alice := testWallet(b)
	bobKey, bob := testWallet(b)
	state, err := ledger.Audit()
	if err != nil {
		b.Fatal(err)
	}
	for i := 0; i < 1024; i++ {
		miner := alice
		var tx *Transaction
		if i > 0 {
			key := aliceKey
			to := bob
			if i%2 == 0 {
				key, miner, to = bobKey, bob, alice
			}
			tx = testSign(b, ledger.Network, key, to, 1, state.Accounts[miner].Nonce+1)
		}
		block := Block{Height: state.Height + 1, Previous: state.Tip, Miner: miner, Transfer: tx}
		for block.Nonce < maxAttempts {
			digest := block.digest(ledger.Network)
			if digest[0] == 0 {
				block.Hash = hex.EncodeToString(digest[:])
				break
			}
			block.Nonce++
		}
		if err := block.verify(state); err != nil {
			b.Fatal(err)
		}
		ledger.Blocks = append(ledger.Blocks, block)
	}
	b.ReportAllocs()
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		if _, err := ledger.Audit(); err != nil {
			b.Fatal(err)
		}
	}
}
