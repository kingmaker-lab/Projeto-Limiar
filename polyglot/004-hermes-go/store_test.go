package main

import (
	"net/http/httptest"
	"path/filepath"
	"strings"
	"sync"
	"testing"
)

func TestConcurrentPersistence(t *testing.T) {
	path := filepath.Join(t.TempDir(), "messages.json")
	store, err := Open(path)
	if err != nil {
		t.Fatal(err)
	}
	var workers sync.WaitGroup
	for i := 0; i < 8; i++ {
		workers.Add(1)
		go func() {
			defer workers.Done()
			if _, err := store.Publish("hello"); err != nil {
				t.Error(err)
			}
		}()
	}
	workers.Wait()
	restored, err := Open(path)
	if err != nil {
		t.Fatal(err)
	}
	messages := restored.List(6)
	if len(messages) != 2 || messages[0].ID != 7 || messages[1].ID != 8 {
		t.Fatal(messages)
	}
}

func TestHTTP(t *testing.T) {
	store, err := Open(filepath.Join(t.TempDir(), "messages.json"))
	if err != nil {
		t.Fatal(err)
	}
	for _, test := range []struct {
		method, path, body string
		code               int
	}{
		{"POST", "/messages", `{"text":"hi"}`, 201},
		{"POST", "/messages", `{"text":" "}`, 400},
		{"GET", "/messages?after=0", "", 200},
		{"GET", "/messages?after=-1", "", 400},
	} {
		response := httptest.NewRecorder()
		handler(store).ServeHTTP(response, httptest.NewRequest(test.method, test.path, strings.NewReader(test.body)))
		if response.Code != test.code {
			t.Fatalf("%s: %d", test.path, response.Code)
		}
	}
}
