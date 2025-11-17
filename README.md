
# init-service

A python library to initialise a repository.

This library,
- clones an existing repository
- adds the Play project with up to date dependencies
- commits and pushes the changes to Github

Run `init-service --help` for instructions.

## Prerequisites

This library requires,
- Python 3.9
- the `$WORKSPACE` environment variable to be set - new repositories will be created
in this directory
- a github token with permissions to push to the repository that needs initialising

### Additional development dependencies

- poetry ( `pip install poetry` )

To install the dependencies run:
```make init```

Or if you have nix installed, you can just run `nix-shell`

## Installation

```pip install -i https://artefacts.tax.service.gov.uk/artifactory/api/pypi/pips/simple init-service```
## Example usage

Create a frontend microservice like this:
```init-service my-frontend-microservice FRONTEND --github-token <token>```

Create a backend microservice like this:
```init-service my-backend-microservice BACKEND --with-mongo --github-token <token>```

## Running the tests

In order to run the tests you will need [pytest](https://docs.pytest.org/) installed.

To run the tests run:
```make test```

## Manually testing a new repository

You can generate a repository for inspection with:
```init-service <repository-name> <type>  --dry-run```

The new repository will be created in `$WORKSPACE/`

You will then need to manually copy over the `repository.yaml` and
`LICENSE` file (public repositories only) from another HMRC repository.

For example,

```bash
init-service test-frontend FRONTEND
cp ../contact-frontend/LICENSE ../test-frontend
cp ../contact-frontend/repository.yaml ../test-frontend
cd ../test-frontend
sbt run
```

Then navigate to http://localhost:9000/test-frontend

## Adding a file specific to a backend or a frontend

If you need to add a file that should only exist in a frontend or backend, but not both, add the
path to the file to `templates/service/template/BACKEND.delete` if frontend-specific or
`templates/service/template/FRONTEND.delete` if backend-specific.

## Publishing a new version

Increment the version found in pyproject.toml and run:

```bash
make publish
```

## CI/CD Build Process

The build process is managed through Jenkins and is defined in the [build-jobs repository](https://github.com/hmrc/build-jobs/blob/main/jobs/live/platops.groovy#L178).

### Pull Request Build

When a pull request is opened:
- Runs `make test` to execute unit tests

### Main Branch Build

When a PR is merged to `main`:
- Runs `make publish` which:
  1. Runs `make test` to execute unit tests
  2. Runs `make bandit` for security scanning
  3. Builds the package (`poetry build`)
  4. Publishes to Artifactory (`poetry publish`)
- Extracts version using `poetry version --short`
- Tags the repository with the version number

The build uses credentials stored in Jenkins under `hmrc-pips-local-writer-token` for Artifactory authentication.

For more details, see the [platops.groovy configuration](https://github.com/hmrc/build-jobs/blob/main/jobs/live/platops.groovy#L178).
