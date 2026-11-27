package main

import (
	"fmt"
	"regexp"
	"slices"
)

var identifier = regexp.MustCompile(`^[A-Za-z0-9_-]{1,64}$`)

func Plan(graph map[string][]string) ([][]string, error) {
	if len(graph) == 0 || len(graph) > 10000 {
		return nil, fmt.Errorf("expected 1 to 10000 tasks")
	}
	remaining := make(map[string]int, len(graph))
	dependents := make(map[string][]string, len(graph))
	ready := []string{}
	edges := 0
	for task, dependencies := range graph {
		if !identifier.MatchString(task) {
			return nil, fmt.Errorf("invalid task %q", task)
		}
		edges += len(dependencies)
		if edges > 100000 {
			return nil, fmt.Errorf("too many dependencies")
		}
		if len(dependencies) == 0 {
			ready = append(ready, task)
		}
		remaining[task] = len(dependencies)
		seen := map[string]bool{}
		for _, dependency := range dependencies {
			if _, exists := graph[dependency]; !exists || seen[dependency] {
				return nil, fmt.Errorf("%s: missing or repeated dependency %q", task, dependency)
			}
			seen[dependency] = true
			dependents[dependency] = append(dependents[dependency], task)
		}
	}
	var waves [][]string
	completed := 0
	for len(ready) > 0 {
		slices.Sort(ready)
		waves = append(waves, ready)
		completed += len(ready)
		next := []string{}
		for _, task := range ready {
			for _, dependent := range dependents[task] {
				remaining[dependent]--
				if remaining[dependent] == 0 {
					next = append(next, dependent)
				}
			}
		}
		ready = next
	}
	if completed != len(graph) {
		blocked := []string{}
		for task, dependencies := range remaining {
			if dependencies > 0 {
				blocked = append(blocked, task)
			}
		}
		slices.Sort(blocked)
		return nil, fmt.Errorf("cycle detected; blocked tasks: %v", blocked)
	}
	return waves, nil
}
