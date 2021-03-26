
# init-service

A python script to initialise a repository.

This script,
- clones an existing repository
- adds the Play project with up to date dependencies
- commits and pushes the changes to Github

Run `python ./scripts/bin/create.py -h` for instructions.

## Prerequisites

This script requires,
- Python 2.7
- the `$WORKSPACE` environment variable to be set - new repositories will be created
in this directory
- a github token with permissions to push to the repository that needs initialising

## Example usage

Create a frontend microservice like this:
```python scripts/bin/create.py --type FRONTEND --github --github-token <token> my-frontend-microservice```

Create a backend microservice like this:
```python scripts/bin/create.py --type BACKEND --github --with-mongo --github-token <token> my-backend-microservice```

## Running the tests

In order to run the tests you will need [pytest](https://docs.pytest.org/) installed.

To run the tests,

```
cd scripts
./run_tests.sh
```

## Manually testing a new repository

You can generate a repository for inspection with:
```python scripts/bin/create.py --type <type> <repository-name>```

The new repository will be created in `$WORKSPACE/`

You will then need to manually copy over the `repository.yaml` and 
`LICENSE` file (public repositories only) from another HMRC repository.

For example,

```
python scripts/bin/create.py --type FRONTEND test-frontend
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
