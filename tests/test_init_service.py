import init_service

import pytest

import os
import sys
import yaml
import shutil
import subprocess

cwd = os.path.dirname(os.path.realpath(__file__))
os.environ["WORKSPACE"] = cwd


def test_init_service_with_missing_positional_args(mocker):
    mocker.patch.object(
        sys, "argv", ["init-service", "FRONTEND", "--github-token", "ghp_fooToken", "--dry-run"]
    )
    with pytest.raises(SystemExit) as system_exit:
        init_service.run_cli()
    assert system_exit.value.code == 2


@pytest.mark.parametrize(
    "args",
    [
        [
            "init-service",
            "foo-service-frontend",
            "FRONTEND",
            "--github-token",
            "ghp_fooToken",
            "--dry-run",
        ],
        [
            "init-service",
            "foo-service-frontend-mongo",
            "FRONTEND",
            "--github-token",
            "ghp_fooToken",
            "--with-mongo",
            "--dry-run",
        ],
        [
            "init-service",
            "foo-service-backend",
            "BACKEND",
            "--github-token",
            "ghp_fooToken",
            "--dry-run",
        ],
        [
            "init-service",
            "foo-service-backend-mongo",
            "BACKEND",
            "--github-token",
            "ghp_fooToken",
            "--with-mongo",
            "--dry-run",
        ],
        [
            "init-service",
            "foo-service-library",
            "LIBRARY",
            "--github-token",
            "ghp_fooToken",
            "--dry-run",
        ],
        [
            "init-service",
            "foo-service-api",
            "API",
            "--github-token",
            "ghp_fooToken",
            "--dry-run",
        ],
        [
            "init-service",
            "foo-service-api-mongo",
            "API",
            "--github-token",
            "ghp_fooToken",
            "--with-mongo",
            "--dry-run",
        ],
    ],
)
def test_init_service_with_type_service_successfully_runs(mocker, args):
    name, type = args[1], args[2]
    mocker.patch.object(sys, "argv", args)
    add_fake_repository_yaml(name)
    with pytest.raises(SystemExit) as system_exit:
        init_service.run_cli()
    assert system_exit.value.code == 0

    assert_code_compiles(name, "test; it:test") if type != "LIBRARY" else assert_code_compiles(
        name, "test"
    )

    assert_repository_yaml_correct(name, type)

    shutil.rmtree(f"{cwd}/{name}")


def test_init_service_push_repo_arguments(mocker):
    mock_subprocess_popen = mocker.Mock()
    mock_subprocess_popen.return_value.returncode = 0
    patched_subprocess_popen = mocker.patch(
        "init_service.init_service.subprocess.Popen", return_value=mock_subprocess_popen()
    )

    service = init_service.InitService(
        repository="foo-repo",
        type="FRONTEND",
        dry_run=True,
        github_token="foo-github-token",
        with_mongo=True,
        default_branch="foo-default-branch",
    )
    service.push_repo()

    assert patched_subprocess_popen.mock_calls[0].args[0] == [
        "git",
        "push",
        "-u",
        "origin",
        "foo-default-branch",
    ]


def assert_code_compiles(name, command):
    print(f'calling "sbt {command}foo-service" on ')
    process = subprocess.Popen(["sbt", command], cwd=f"{cwd}/{name}")
    o, e = process.communicate()
    print(str(o))
    print(f"return code was {str(process.returncode)}")

    if process.returncode != 0:
        return False
    return True


def assert_repository_yaml_correct(name, repository_type):
    with open(f"{cwd}/{name}" + "/repository.yaml", "r") as repository_yaml:
        yaml_content = yaml.safe_load(repository_yaml)

    if repository_type == "FRONTEND":
        assert yaml_content["type"] == "service"
        assert yaml_content["service-type"] == "frontend"
        assert yaml_content["tags"] == []
    elif repository_type == "BACKEND":
        assert yaml_content["type"] == "service"
        assert yaml_content["service-type"] == "backend"
        assert yaml_content["tags"] == []
    elif repository_type == "API":
        assert yaml_content["type"] == "service"
        assert yaml_content["service-type"] == "backend"
        assert yaml_content["tags"] == ["api"]
    elif repository_type == "LIBRARY":
        assert yaml_content["type"] == "library"


def add_fake_repository_yaml(name):
    print(f"adding fake repository.yaml to {cwd}/{name}")
    os.makedirs(f"{cwd}/{name}", exist_ok=True)
    with open(f"{cwd}/{name}" + "/repository.yaml", "w") as yaml:
        yaml.write(
            "repoVisibility: private_12E5349CFB8BBA30AF464C24760B70343C0EAE9E9BD99156345DD0852C2E0F6F"
        )
