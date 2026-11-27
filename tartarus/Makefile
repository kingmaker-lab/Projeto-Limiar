.PHONY: start list run validate

PYTHON ?= python3

start:
	@$(PYTHON) -B telemetry/replay.py

list:
	@$(PYTHON) -B run.py --list

run:
	@$(PYTHON) -B run.py $(TAR)

validate:
	$(PYTHON) -B -m unittest discover -s telemetry -v
	$(PYTHON) -B -m unittest discover -s tests -v
