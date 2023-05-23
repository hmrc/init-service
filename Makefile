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
	poetry config repositories.artifactory "https://artefacts.tax.service.gov.uk/artifactory/api/pypi/pips/"
	@poetry config http-basic.artifactory ${ARTIFACTORY_USERNAME} ${ARTIFACTORY_PASSWORD}
	@poetry publish --repository artifactory
	poetry run cut-release
	poetry config http-basic.artifactory --unset
	poetry config repositories.artifactory --unset

.PHONY: test
test: init black
	poetry run pytest tests/

.PHONY: update
update: init
	poetry update
