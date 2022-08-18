import click

from .init_service import InitService


@click.command
@click.argument("repository")
@click.argument("type")
@click.option("--dry-run", help="Enable to create repository locally", is_flag=True)
@click.option("--github-token", help="Token to push to GitHub")
@click.option("--with-mongo", help="Use to indicate that a service required mongo", is_flag=True)
@click.option("--default-branch", help="Determine default branch", default="main")
@click.version_option()
def run_cli(repository, type, dry_run, github_token, with_mongo, default_branch):
    service = InitService(repository, type, dry_run, github_token, with_mongo, default_branch)
    service.create_project()
