package main

import (
	"encoding/json"
	"errors"
	"flag"
	"io"
	"log"
	"net/http"
	"strconv"
	"time"
)

func handler(store *Store) http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /messages", func(w http.ResponseWriter, r *http.Request) {
		after := 0
		if cursor := r.URL.Query().Get("after"); cursor != "" {
			parsed, err := strconv.Atoi(cursor)
			if err != nil || parsed < 0 {
				http.Error(w, "invalid cursor", 400)
				return
			}
			after = parsed
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(store.List(after))
	})
	mux.HandleFunc("POST /messages", func(w http.ResponseWriter, r *http.Request) {
		var input struct {
			Text string `json:"text"`
		}
		decoder := json.NewDecoder(http.MaxBytesReader(w, r.Body, 32768))
		decoder.DisallowUnknownFields()
		if decoder.Decode(&input) != nil || decoder.Decode(new(any)) != io.EOF || !valid(input.Text) {
			http.Error(w, "invalid message", 400)
			return
		}
		message, err := store.Publish(input.Text)
		if errors.Is(err, errFull) {
			http.Error(w, err.Error(), 409)
			return
		}
		if err != nil {
			log.Print(err)
			http.Error(w, "persistence failed", 500)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(201)
		_ = json.NewEncoder(w).Encode(message)
	})
	return mux
}

func main() {
	path := flag.String("file", "messages.json", "snapshot path")
	port := flag.Uint("port", 8080, "loopback port")
	flag.Parse()
	if *port == 0 || *port > 65535 {
		log.Fatal("invalid port")
	}
	store, err := Open(*path)
	if err != nil {
		log.Fatal(err)
	}
	server := &http.Server{Addr: "127.0.0.1:" + strconv.FormatUint(uint64(*port), 10),
		Handler: handler(store), ReadTimeout: 5 * time.Second, WriteTimeout: 10 * time.Second}
	log.Fatal(server.ListenAndServe())
}
