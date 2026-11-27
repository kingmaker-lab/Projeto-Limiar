package atlas

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"syscall"
)

const maxLedgerBytes = 8 << 20

func ReadJSON(path string, limit int64, dst any) error {
	file, err := os.Open(path)
	if err != nil {
		return err
	}
	defer file.Close()
	info, err := file.Stat()
	if err != nil {
		return err
	}
	if !info.Mode().IsRegular() || info.Size() > limit {
		return errors.New("tipo ou tamanho de arquivo inválido")
	}
	return decodeJSON(file, limit, dst)
}

func decodeJSON(source io.Reader, limit int64, dst any) error {
	reader := &io.LimitedReader{R: source, N: limit + 1}
	decoder := json.NewDecoder(reader)
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(dst); err != nil {
		return err
	}
	var trailing any
	if err := decoder.Decode(&trailing); err != io.EOF || reader.N == 0 {
		return errors.New("JSON excede o limite ou contém dados adicionais")
	}
	return nil
}

func Load(dir string) (*Ledger, error) {
	var ledger Ledger
	if err := ReadJSON(filepath.Join(dir, "ledger.json"), maxLedgerBytes, &ledger); err != nil {
		return nil, err
	}
	return &ledger, nil
}

// Update serializes every writer using the directory inode, which remains
// stable when ledger.json is replaced. A nil result skips the write.
func Update(dir string, update func(*Ledger) (*Ledger, error)) error {
	lock, err := os.Open(dir)
	if err != nil {
		return err
	}
	defer lock.Close()
	if err := syscall.Flock(int(lock.Fd()), syscall.LOCK_EX); err != nil {
		return err
	}
	ledger, err := Load(dir)
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		return err
	}
	next, err := update(ledger)
	if err != nil || next == nil {
		return err
	}
	if _, err := next.Audit(); err != nil {
		return err
	}
	data, err := json.Marshal(next)
	if err != nil {
		return err
	}
	return WriteFile(filepath.Join(dir, "ledger.json"), append(data, '\n'), true)
}

func WriteFile(path string, data []byte, replace bool) error {
	dir, err := os.Open(filepath.Dir(path))
	if err != nil {
		return err
	}
	defer dir.Close()
	file, err := os.CreateTemp(dir.Name(), ".atlas-*")
	if err != nil {
		return err
	}
	defer os.Remove(file.Name())
	defer file.Close()
	if _, err := file.Write(data); err != nil {
		return err
	}
	if err := file.Sync(); err != nil {
		return err
	}
	if err := file.Close(); err != nil {
		return err
	}
	if replace {
		err = os.Rename(file.Name(), path)
	} else {
		err = os.Link(file.Name(), path)
	}
	if err != nil {
		return err
	}
	if err := dir.Sync(); err != nil {
		return fmt.Errorf("arquivo gravado, mas a confirmação em disco falhou: %w", err)
	}
	return nil
}
