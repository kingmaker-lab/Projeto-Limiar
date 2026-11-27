package atlas

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net"
	"net/http"
	"os"
	"slices"
	"strconv"
	"time"
)

const snapshotPath = "/v1/ledger"

// ServePeer exposes an audited read-only snapshot on IPv4 loopback.
func ServePeer(dir string, port uint16, ready func(string)) error {
	ledger, err := Load(dir)
	if err != nil {
		return err
	}
	if _, err := ledger.Audit(); err != nil {
		return err
	}
	listener, err := net.Listen("tcp4", loopback(port))
	if err != nil {
		return err
	}
	defer listener.Close()
	server := &http.Server{
		Handler:           peerHandler(dir),
		ReadHeaderTimeout: 2 * time.Second,
		ReadTimeout:       5 * time.Second,
		WriteTimeout:      10 * time.Second,
		IdleTimeout:       5 * time.Second,
		MaxHeaderBytes:    8 << 10,
	}
	ready(listener.Addr().String())
	return server.Serve(listener)
}

func loopback(port uint16) string {
	return "127.0.0.1:" + strconv.Itoa(int(port))
}

func peerHandler(dir string) http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET "+snapshotPath, func(w http.ResponseWriter, _ *http.Request) {
		ledger, err := Load(dir)
		if err == nil {
			_, err = ledger.Audit()
		}
		if err != nil {
			http.Error(w, "ledger indisponível", http.StatusServiceUnavailable)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Cache-Control", "no-store")
		_ = json.NewEncoder(w).Encode(ledger)
	})
	return mux
}

// Sync pulls and verifies one snapshot. A network ID received out of band is
// required even when creating a fresh local replica.
func Sync(ctx context.Context, dir string, port uint16, network string) (*State, error) {
	if port == 0 || !validHash(network) {
		return nil, errors.New("porta ou identificador da rede inválido")
	}
	remote, err := fetchSnapshot(ctx, port)
	if err != nil {
		return nil, err
	}
	if remote.Network != network {
		return nil, errors.New("rede do par não corresponde à rede esperada")
	}
	state, err := remote.Audit()
	if err != nil {
		return nil, fmt.Errorf("histórico do par inválido: %w", err)
	}
	if err := os.MkdirAll(dir, 0700); err != nil {
		return nil, err
	}

	err = Update(dir, func(local *Ledger) (*Ledger, error) {
		if local == nil {
			return remote, nil
		}
		if local.Network != network {
			return nil, errors.New("ledger local pertence a outra rede")
		}
		localState, err := local.Audit()
		if err != nil {
			return nil, err
		}
		common := min(len(local.Blocks), len(remote.Blocks))
		sameHash := func(a, b Block) bool { return a.Hash == b.Hash }
		if !slices.EqualFunc(local.Blocks[:common], remote.Blocks[:common], sameHash) {
			return nil, errors.New("históricos divergentes; sincronização recusada")
		}
		if len(remote.Blocks) <= len(local.Blocks) {
			state = localState
			return nil, nil
		}
		return remote, nil
	})
	if err != nil {
		return nil, err
	}
	return state, nil
}

func fetchSnapshot(ctx context.Context, port uint16) (*Ledger, error) {
	transport := &http.Transport{DisableCompression: true, DisableKeepAlives: true, MaxResponseHeaderBytes: 8 << 10}
	client := &http.Client{
		Transport: transport,
		Timeout:   10 * time.Second,
		CheckRedirect: func(_ *http.Request, _ []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, "http://"+loopback(port)+snapshotPath, nil)
	if err != nil {
		return nil, err
	}
	response, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer response.Body.Close()
	if response.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("par respondeu com HTTP %d", response.StatusCode)
	}
	if response.ContentLength > maxLedgerBytes {
		return nil, errors.New("instantâneo excede 8 MiB")
	}
	var ledger Ledger
	if err := decodeJSON(response.Body, maxLedgerBytes, &ledger); err != nil {
		return nil, fmt.Errorf("instantâneo do par: %w", err)
	}
	return &ledger, nil
}
