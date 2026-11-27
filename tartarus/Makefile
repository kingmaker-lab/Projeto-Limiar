.PHONY: start validate

start:
	@python3 telemetry/replay.py

validate:
	python3 -B -m unittest discover -s telemetry -v
