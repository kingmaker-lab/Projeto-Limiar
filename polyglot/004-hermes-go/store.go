package main

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"unicode/utf8"
)

type Message struct {
	ID   int    `json:"id"`
	Text string `json:"text"`
}

type Store struct {
	mu       sync.Mutex
	path     string
	messages []Message
}

var errFull = errors.New("message capacity reached")

func valid(text string) bool {
	return utf8.ValidString(text) && len(text) <= 4096 && strings.TrimSpace(text) != ""
}

func Open(path string) (*Store, error) {
	store := &Store{path: path, messages: []Message{}}
	data, err := os.ReadFile(path)
	if errors.Is(err, os.ErrNotExist) {
		return store, nil
	}
	if err != nil {
		return nil, err
	}
	if err := json.Unmarshal(data, &store.messages); err != nil {
		return nil, err
	}
	if store.messages == nil || len(store.messages) > 1000 {
		return nil, errors.New("invalid snapshot")
	}
	for i, message := range store.messages {
		if message.ID != i+1 || !valid(message.Text) {
			return nil, errors.New("invalid snapshot")
		}
	}
	return store, nil
}

func (s *Store) List(after int) []Message {
	s.mu.Lock()
	defer s.mu.Unlock()
	start := min(max(after, 0), len(s.messages))
	return append([]Message{}, s.messages[start:]...)
}

func (s *Store) Publish(text string) (Message, error) {
	if !valid(text) {
		return Message{}, errors.New("invalid text")
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	if len(s.messages) >= 1000 {
		return Message{}, errFull
	}
	message := Message{len(s.messages) + 1, text}
	next := append(s.messages, message)
	file, err := os.CreateTemp(filepath.Dir(s.path), ".hermes-*")
	if err != nil {
		return Message{}, err
	}
	defer os.Remove(file.Name())
	err = json.NewEncoder(file).Encode(next)
	if err == nil {
		err = file.Sync()
	}
	closeErr := file.Close()
	if err == nil {
		err = closeErr
	}
	if err != nil {
		return Message{}, err
	}
	if err := os.Rename(file.Name(), s.path); err != nil {
		return Message{}, err
	}
	s.messages = next
	return message, nil
}
