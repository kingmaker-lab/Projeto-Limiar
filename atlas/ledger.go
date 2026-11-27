package atlas

import (
	"bytes"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"crypto/x509"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"math/big"
)

const (
	Version     = "ATLAS_GENESIS_V1"
	Reward      = 50
	MaxBlocks   = 4096
	maxAttempts = 500000
)

type Transaction struct {
	From      string `json:"from"`
	To        string `json:"to"`
	Amount    uint64 `json:"amount"`
	Nonce     uint64 `json:"nonce"`
	PublicKey []byte `json:"publicKey"`
	Signature []byte `json:"signature"`
}

type Block struct {
	Height   int          `json:"height"`
	Previous string       `json:"previous"`
	Miner    string       `json:"miner"`
	Transfer *Transaction `json:"transfer"`
	Nonce    uint32       `json:"nonce"`
	Hash     string       `json:"hash"`
}

type Ledger struct {
	Version string  `json:"version"`
	Network string  `json:"network"`
	Blocks  []Block `json:"blocks"`
}

type Account struct {
	Balance uint64 `json:"balance"`
	Nonce   uint64 `json:"nonce"`
}

type State struct {
	Network  string             `json:"network"`
	Height   int                `json:"height"`
	Tip      string             `json:"tip"`
	Supply   uint64             `json:"supply"`
	Accounts map[string]Account `json:"accounts"`
}

func NewLedger() (*Ledger, error) {
	var id [32]byte
	if _, err := rand.Read(id[:]); err != nil {
		return nil, err
	}
	return &Ledger{Version: Version, Network: hex.EncodeToString(id[:]), Blocks: []Block{}}, nil
}

func hash(b []byte) string {
	sum := sha256.Sum256(b)
	return hex.EncodeToString(sum[:])
}

// Protocol arrays contain only ASCII identifiers, integers, null, and base64 bytes.
func encode(fields ...any) []byte {
	data, err := json.Marshal(fields)
	if err != nil {
		panic(err)
	}
	return data
}

func validHash(value string) bool {
	if len(value) != 64 {
		return false
	}
	raw, err := hex.DecodeString(value)
	return err == nil && hex.EncodeToString(raw) == value
}

func validAddress(value string) bool {
	return len(value) == 68 && value[:4] == "atl_" && validHash(value[4:])
}

func Address(key *ecdsa.PublicKey) (string, error) {
	der, err := x509.MarshalPKIXPublicKey(key)
	if err != nil {
		return "", err
	}
	return "atl_" + hash(der), nil
}

// EXP-003 payload ordering derives from the Workshop protocol. The network ID
// scopes a signature to the ledger for which the signer created it.
func (tx Transaction) payload(network string) []byte {
	return encode(Version+"/transfer", network, tx.From, tx.To, tx.Amount, tx.Nonce)
}

func Sign(network string, key *ecdsa.PrivateKey, to string, amount, nonce uint64) (*Transaction, error) {
	if key.Curve != elliptic.P256() || !validHash(network) {
		return nil, errors.New("chave ou rede inválida")
	}
	public, err := x509.MarshalPKIXPublicKey(&key.PublicKey)
	if err != nil {
		return nil, err
	}
	tx := &Transaction{From: "atl_" + hash(public), To: to, Amount: amount, Nonce: nonce, PublicKey: public}
	if !validAddress(to) || tx.From == to || amount == 0 || amount > MaxBlocks*Reward || nonce == 0 || nonce > MaxBlocks {
		return nil, errors.New("transferência inválida")
	}
	digest := sha256.Sum256(tx.payload(network))
	r, s, err := ecdsa.Sign(rand.Reader, key, digest[:])
	if err != nil {
		return nil, err
	}
	tx.Signature = make([]byte, 64)
	r.FillBytes(tx.Signature[:32])
	s.FillBytes(tx.Signature[32:])
	return tx, nil
}

func (tx Transaction) apply(state *State) error {
	if !validAddress(tx.From) || !validAddress(tx.To) || tx.From == tx.To ||
		tx.Amount == 0 || len(tx.PublicKey) != 91 || len(tx.Signature) != 64 {
		return errors.New("formato da transferência inválido")
	}
	from := state.Accounts[tx.From]
	if tx.Nonce != from.Nonce+1 {
		return errors.New("nonce incorreto")
	}
	if from.Balance < tx.Amount {
		return errors.New("saldo insuficiente")
	}
	key, err := x509.ParsePKIXPublicKey(tx.PublicKey)
	public, ok := key.(*ecdsa.PublicKey)
	if err != nil || !ok || public.Curve != elliptic.P256() {
		return errors.New("chave pública inválida")
	}
	der, err := x509.MarshalPKIXPublicKey(public)
	if err != nil || !bytes.Equal(der, tx.PublicKey) || "atl_"+hash(der) != tx.From {
		return errors.New("chave pública não corresponde ao remetente")
	}
	digest := sha256.Sum256(tx.payload(state.Network))
	r := new(big.Int).SetBytes(tx.Signature[:32])
	s := new(big.Int).SetBytes(tx.Signature[32:])
	if !ecdsa.Verify(public, digest[:], r, s) {
		return errors.New("assinatura inválida")
	}
	to := state.Accounts[tx.To]
	from.Balance -= tx.Amount
	from.Nonce++
	to.Balance += tx.Amount
	state.Accounts[tx.From], state.Accounts[tx.To] = from, to
	return nil
}

// Like EXP-002, the header uses a positional JSON array and SHA-256. The
// transfer commitment also covers the public key and the raw signature.
func (b Block) digest(network string) [32]byte {
	var transfer any
	if tx := b.Transfer; tx != nil {
		transfer = []any{tx.From, tx.To, tx.Amount, tx.Nonce, tx.PublicKey, tx.Signature}
	}
	return sha256.Sum256(encode(Version+"/block", network, b.Height, b.Previous, b.Miner, transfer, b.Nonce))
}

func (b Block) verify(state *State) error {
	if b.Height != state.Height+1 || b.Previous != state.Tip || !validAddress(b.Miner) || b.Nonce >= maxAttempts {
		return errors.New("cabeçalho inválido")
	}
	if tx := b.Transfer; tx != nil {
		if err := tx.apply(state); err != nil {
			return err
		}
	}
	digest := b.digest(state.Network)
	if digest[0] != 0 || hex.EncodeToString(digest[:]) != b.Hash {
		return errors.New("prova de trabalho inválida")
	}
	miner := state.Accounts[b.Miner]
	miner.Balance += Reward
	state.Accounts[b.Miner] = miner
	state.Height, state.Tip = b.Height, b.Hash
	state.Supply += Reward
	return nil
}

func (l *Ledger) Audit() (*State, error) {
	if l.Version != Version || !validHash(l.Network) || l.Blocks == nil || len(l.Blocks) > MaxBlocks {
		return nil, errors.New("ledger inválido")
	}
	state := &State{
		Network:  l.Network,
		Tip:      hash(encode(Version+"/genesis", l.Network)),
		Accounts: make(map[string]Account),
	}
	for index, b := range l.Blocks {
		if err := b.verify(state); err != nil {
			return nil, fmt.Errorf("bloco %d: %w", index+1, err)
		}
	}
	return state, nil
}

func (l *Ledger) Mine(miner string, tx *Transaction) (Block, error) {
	state, err := l.Audit()
	if err != nil {
		return Block{}, err
	}
	if state.Height == MaxBlocks || !validAddress(miner) {
		return Block{}, errors.New("limite de blocos atingido ou minerador inválido")
	}
	if tx != nil {
		if err := tx.apply(state); err != nil {
			return Block{}, err
		}
		// The signed bytes become part of the ledger and must not alias the caller.
		copyTx := *tx
		copyTx.PublicKey = bytes.Clone(tx.PublicKey)
		copyTx.Signature = bytes.Clone(tx.Signature)
		tx = &copyTx
	}
	block := Block{Height: state.Height + 1, Previous: state.Tip, Miner: miner, Transfer: tx}
	for block.Nonce = 0; block.Nonce < maxAttempts; block.Nonce++ {
		digest := block.digest(l.Network)
		if digest[0] == 0 {
			block.Hash = hex.EncodeToString(digest[:])
			l.Blocks = append(l.Blocks, block)
			if tx != nil {
				return cloneBlock(block), nil
			}
			return block, nil
		}
	}
	return Block{}, errors.New("limite de tentativas de mineração atingido")
}

func cloneBlock(block Block) Block {
	tx := *block.Transfer
	tx.PublicKey = bytes.Clone(tx.PublicKey)
	tx.Signature = bytes.Clone(tx.Signature)
	block.Transfer = &tx
	return block
}
