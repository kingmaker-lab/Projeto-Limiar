package main

import (
	"bytes"
	"strings"
	"testing"
)

func TestWaves(t *testing.T) {
	var output bytes.Buffer
	if err := run(strings.NewReader(`{"c":["a","b"],"b":[],"a":[],"d":["c"]}`), &output); err != nil {
		t.Fatal(err)
	}
	if output.String() != "[[\"a\",\"b\"],[\"c\"],[\"d\"]]\n" {
		t.Fatal(output.String())
	}
}

func TestInvalidGraph(t *testing.T) {
	for _, input := range []string{`{"a":["b"],"b":["a"]}`, `{"a":["missing"]}`, `{"a":[],"b":["a","a"]}`, `{"a":[],"a":[]}`, `{"a":null}`} {
		if err := run(strings.NewReader(input), &bytes.Buffer{}); err == nil {
			t.Fatal(input)
		}
	}
}
