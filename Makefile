.PHONY: fmt
fmt:
	ruff format src tests

.PHONY: lint
lint:
	ruff check src tests
	mypy src tests
	ruff format --check src tests

.PHONY: test
test:
	pytest --verbose

.PHONY: clean-docs
clean-docs:
	rm -rf docs

.PHONY: docs
docs: clean-docs
	mkdir -p docs \
	&& pdoc --html --output-dir docs extreqs
