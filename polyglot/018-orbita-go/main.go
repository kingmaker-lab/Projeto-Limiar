package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
)

func run(input io.Reader, output io.Writer) error {
	const limit = 4 << 20
	data, err := io.ReadAll(io.LimitReader(input, limit+1))
	if err != nil {
		return err
	}
	if len(data) > limit {
		return fmt.Errorf("input exceeds 4 MiB")
	}
	graph, err := decodeGraph(data)
	if err != nil {
		return err
	}
	waves, err := Plan(graph)
	if err != nil {
		return err
	}
	return json.NewEncoder(output).Encode(waves)
}

func decodeGraph(data []byte) (map[string][]string, error) {
	decoder := json.NewDecoder(bytes.NewReader(data))
	if opening, err := decoder.Token(); err != nil || opening != json.Delim('{') {
		return nil, fmt.Errorf("expected JSON object")
	}
	graph := map[string][]string{}
	for decoder.More() {
		key, err := decoder.Token()
		task, valid := key.(string)
		if err != nil || !valid {
			return nil, fmt.Errorf("expected a task name")
		}
		if _, exists := graph[task]; exists {
			return nil, fmt.Errorf("duplicate task %q", task)
		}
		var dependencies []string
		if err := decoder.Decode(&dependencies); err != nil || dependencies == nil {
			return nil, fmt.Errorf("%s: expected array of dependency names", task)
		}
		graph[task] = dependencies
	}
	if closing, err := decoder.Token(); err != nil || closing != json.Delim('}') {
		return nil, fmt.Errorf("incomplete JSON object")
	}
	if _, err := decoder.Token(); err != io.EOF {
		return nil, fmt.Errorf("unexpected data after JSON object")
	}
	return graph, nil
}

func main() {
	if err := run(os.Stdin, os.Stdout); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
}
