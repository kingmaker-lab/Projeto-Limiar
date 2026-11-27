package main

import (
	"context"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/x509"
	"encoding/json"
	"encoding/pem"
	"errors"
	"flag"
	"fmt"
	"os"
	"strconv"

	"github.com/kingmaker-lab/Projeto-Limiar/atlas"
)

const usage = `atlas [-dir DIRETÓRIO] init
atlas wallet ARQUIVO
atlas [-dir DIRETÓRIO] status
atlas [-dir DIRETÓRIO] serve PORTA
atlas [-dir DIRETÓRIO] sync PORTA REDE
atlas [-dir DIRETÓRIO] mine ENDEREÇO [TRANSFERÊNCIA.json]
atlas [-dir DIRETÓRIO] sign CARTEIRA DESTINO VALOR > TRANSFERÊNCIA.json`

func main() {
	dir := flag.String("dir", ".atlas", "diretório privado do ledger")
	flag.Usage = func() { fmt.Fprintln(os.Stderr, usage) }
	flag.Parse()
	if err := run(*dir, flag.Args()); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func run(dir string, args []string) error {
	switch {
	case len(args) == 1 && args[0] == "init":
		if err := os.MkdirAll(dir, 0700); err != nil {
			return err
		}
		return atlas.Update(dir, func(current *atlas.Ledger) (*atlas.Ledger, error) {
			if current != nil {
				return nil, errors.New("ledger já existe")
			}
			return atlas.NewLedger()
		})
	case len(args) == 2 && args[0] == "wallet":
		return wallet(args[1])
	case len(args) == 1 && args[0] == "status":
		ledger, err := atlas.Load(dir)
		if err != nil {
			return err
		}
		state, err := ledger.Audit()
		if err != nil {
			return err
		}
		return json.NewEncoder(os.Stdout).Encode(state)
	case len(args) == 2 && args[0] == "serve":
		port, err := parsePort(args[1])
		if err != nil {
			return err
		}
		return atlas.ServePeer(dir, port, func(address string) { fmt.Println(address) })
	case len(args) == 3 && args[0] == "sync":
		port, err := parsePort(args[1])
		if err != nil {
			return err
		}
		state, err := atlas.Sync(context.Background(), dir, port, args[2])
		if err != nil {
			return err
		}
		return json.NewEncoder(os.Stdout).Encode(state)
	case len(args) >= 2 && len(args) <= 3 && args[0] == "mine":
		return mine(dir, args[1:])
	case len(args) == 4 && args[0] == "sign":
		return sign(dir, args[1], args[2], args[3])
	default:
		return errors.New(usage)
	}
}

func parsePort(value string) (uint16, error) {
	port, err := strconv.ParseUint(value, 10, 16)
	if err != nil {
		return 0, fmt.Errorf("porta inválida: %w", err)
	}
	return uint16(port), nil
}

func wallet(path string) error {
	key, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		return err
	}
	der, err := x509.MarshalECPrivateKey(key)
	if err != nil {
		return err
	}
	data := pem.EncodeToMemory(&pem.Block{Type: "EC PRIVATE KEY", Bytes: der})
	if err := atlas.WriteFile(path, data, false); err != nil {
		return err
	}
	address, err := atlas.Address(&key.PublicKey)
	if err != nil {
		return err
	}
	_, err = fmt.Println(address)
	return err
}

func sign(dir, path, to, amountText string) error {
	amount, err := strconv.ParseUint(amountText, 10, 64)
	if err != nil {
		return fmt.Errorf("valor inválido: %w", err)
	}
	data, err := os.ReadFile(path)
	if err != nil {
		return err
	}
	block, remainder := pem.Decode(data)
	if block == nil || block.Type != "EC PRIVATE KEY" || len(remainder) != 0 {
		return errors.New("arquivo de carteira inválido")
	}
	key, err := x509.ParseECPrivateKey(block.Bytes)
	if err != nil {
		return err
	}
	ledger, err := atlas.Load(dir)
	if err != nil {
		return err
	}
	state, err := ledger.Audit()
	if err != nil {
		return err
	}
	from, err := atlas.Address(&key.PublicKey)
	if err != nil {
		return err
	}
	account := state.Accounts[from]
	if account.Balance < amount {
		return errors.New("saldo insuficiente")
	}
	tx, err := atlas.Sign(state.Network, key, to, amount, account.Nonce+1)
	if err != nil {
		return err
	}
	return json.NewEncoder(os.Stdout).Encode(tx)
}

func mine(dir string, args []string) error {
	var transfer *atlas.Transaction
	if len(args) == 2 {
		transfer = new(atlas.Transaction)
		if err := atlas.ReadJSON(args[1], 4096, transfer); err != nil {
			return err
		}
	}
	var block atlas.Block
	err := atlas.Update(dir, func(ledger *atlas.Ledger) (*atlas.Ledger, error) {
		if ledger == nil {
			return nil, errors.New("execute init primeiro")
		}
		var err error
		block, err = ledger.Mine(args[0], transfer)
		return ledger, err
	})
	if err != nil {
		return err
	}
	return json.NewEncoder(os.Stdout).Encode(block)
}
