package atlas

import (
	"bytes"
	"encoding/json"
	"net"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"testing"
)

func peerPort(t *testing.T, handler http.Handler) uint16 {
	t.Helper()
	listener, err := net.Listen("tcp4", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}
	server := &httptest.Server{Listener: listener, Config: &http.Server{Handler: handler}}
	server.Start()
	t.Cleanup(server.Close)
	return uint16(listener.Addr().(*net.TCPAddr).Port)
}

func saveLedger(t *testing.T, dir string, ledger *Ledger) {
	t.Helper()
	if err := Update(dir, func(*Ledger) (*Ledger, error) { return ledger, nil }); err != nil {
		t.Fatal(err)
	}
}

func TestPeerSync(t *testing.T) {
	key, alice := testWallet(t)
	_, bob := testWallet(t)
	origin, replica := t.TempDir(), t.TempDir()
	ledger := testLedger(t, alice)
	saveLedger(t, origin, ledger)
	port := peerPort(t, peerHandler(origin))
	state, err := Sync(t.Context(), replica, port, ledger.Network)
	if err != nil || state.Height != 1 {
		t.Fatalf("primeira sincronização: estado=%+v erro=%v", state, err)
	}
	if _, err := ledger.Mine(alice, testSign(t, ledger.Network, key, bob, 17, 1)); err != nil {
		t.Fatal(err)
	}
	saveLedger(t, origin, ledger)
	// A new connection and fresh disk load simulate restarting the source.
	restartedPort := peerPort(t, peerHandler(origin))
	state, err = Sync(t.Context(), replica, restartedPort, ledger.Network)
	if err != nil || state.Height != 2 || state.Supply != 100 || state.Accounts[bob].Balance != 17 {
		t.Fatalf("segunda sincronização: estado=%+v erro=%v", state, err)
	}
	replicaPath := filepath.Join(replica, "ledger.json")
	before, err := os.ReadFile(replicaPath)
	if err != nil {
		t.Fatal(err)
	}
	state, err = Sync(t.Context(), replica, restartedPort, ledger.Network)
	if err != nil || state.Height != 2 {
		t.Fatalf("sincronização repetida: estado=%+v erro=%v", state, err)
	}

	// A stale prefix is harmless. A conflicting block is rejected even when both forks validate.
	ledger.Blocks = ledger.Blocks[:1]
	saveLedger(t, origin, ledger)
	state, err = Sync(t.Context(), replica, restartedPort, ledger.Network)
	if err != nil || state.Height != 2 {
		t.Fatalf("par atrasado: estado=%+v erro=%v", state, err)
	}
	if _, err := ledger.Mine(bob, nil); err != nil {
		t.Fatal(err)
	}
	saveLedger(t, origin, ledger)
	if _, err := Sync(t.Context(), replica, restartedPort, ledger.Network); err == nil || !strings.Contains(err.Error(), "divergentes") {
		t.Fatalf("fork aceito: %v", err)
	}
	after, err := os.ReadFile(replicaPath)
	if err != nil || !bytes.Equal(before, after) {
		t.Fatalf("réplica alterada: %v", err)
	}
}

func TestPeerRejectsInvalidSnapshot(t *testing.T) {
	_, miner := testWallet(t)
	ledger := testLedger(t, miner)
	bad := *ledger
	bad.Blocks = append([]Block(nil), ledger.Blocks...)
	bad.Blocks[0].Hash = strings.Repeat("0", 64)
	serveLedger := func(l *Ledger) http.HandlerFunc {
		return func(w http.ResponseWriter, _ *http.Request) { _ = json.NewEncoder(w).Encode(l) }
	}
	for _, tc := range []struct {
		name    string
		network string
		handler http.HandlerFunc
		want    string
	}{
		{"rede", strings.Repeat("a", 64), serveLedger(ledger), "rede do par"},
		{"prova", ledger.Network, serveLedger(&bad), "histórico do par inválido"},
		{"redirecionamento", ledger.Network, func(w http.ResponseWriter, r *http.Request) {
			http.Redirect(w, r, "/redirect", http.StatusFound)
		}, "HTTP 302"},
		{"tamanho", ledger.Network, func(w http.ResponseWriter, _ *http.Request) {
			w.Header().Set("Content-Length", strconv.Itoa(maxLedgerBytes+1))
			w.WriteHeader(http.StatusOK)
		}, "excede 8 MiB"},
		{"conteúdo adicional", ledger.Network, func(w http.ResponseWriter, _ *http.Request) {
			_ = json.NewEncoder(w).Encode(ledger)
			_, _ = w.Write([]byte("{}"))
		}, "dados adicionais"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			dir := t.TempDir()
			port := peerPort(t, tc.handler)
			if _, err := Sync(t.Context(), dir, port, tc.network); err == nil || !strings.Contains(err.Error(), tc.want) {
				t.Fatalf("resposta inválida aceita: %v", err)
			}
			if _, err := os.Stat(filepath.Join(dir, "ledger.json")); !os.IsNotExist(err) {
				t.Fatalf("gravação inesperada: %v", err)
			}
		})
	}
}
