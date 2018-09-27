
# init-service

A python script to initialise a repository

Run `python ./scripts/bin/create.py -h` for instructions.

The script requires a "WORKSPACE" environment variable to be set.
The script requires a github token with permissions to push to the repository that need initialising

This will:
- clone an existing repository
- add the play project with up to date dependencies
- commit and push the changes

####Examples

Create a frontend microservice like this:
```python scripts/bin/create.py --type FRONTEND --exists --github_token <token> my-backend-microservice```

Create a backend microservice like this:
```python scripts/bin/create.py --type BACKEND --exists --use_mongo --github_token <token> my-backend-microservice```