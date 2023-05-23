.PHONY: bandit
bandit:
	poetry run bandit -c pyproject.toml --recursive .

.PHONY: black
black:
	poetry run black . --config=./pyproject.toml

.PHONY: build
build: test bandit
	poetry build

.PHONY: init
init:
	pip install --index-url https://artefacts.tax.service.gov.uk/artifactory/api/pypi/pips/simple/ poetry
	poetry install
#    poetry run pre-commit install

# Increment the version found in pyproject.toml for a new release
.PHONY: publish
publish: build
	@poetry config pypi-token.artefacts ${ARTIFACTORY_PASSWORD}
	@poetry publish --repository artefacts

.PHONY: test
test: init black
	poetry run pytest tests/

.PHONY: update
update: init
	poetry update
