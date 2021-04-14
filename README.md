
# init-service

A python script to initialise a repository

Run `python ./scripts/bin/create.py -h` for instructions.

The script requires a "WORKSPACE" environment variable to be set.
The script requires a github token with permissions to push to the repository that need initialising

This will:
- clone an existing repository
- add the play project with up to date dependencies
- commit and push the changes

#### Examples

Create a frontend microservice like this:
```python scripts/bin/create.py --type FRONTEND --github --github-token <token> my-frontend-microservice```

Create a backend microservice like this:
```python scripts/bin/create.py --type BACKEND --github --with-mongo --github-token <token> my-backend-microservice```


#### Testing

You can generate a new local project for inspection with:
```python scripts/bin/create.py --type <type> <project-name>```
