# must set bash, or source is not available!
SHELL := /bin/bash

check:generateBookSummaries.py
	. .venv/bin/activate && . ~/set.openai.key && python $^
