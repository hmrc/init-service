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
    with pytest.raises(SystemExit) as system_exit:
        init_service.run_cli()
    assert system_exit.value.code == 0

    assert_code_compiles(name, "test; it:test") if type != "LIBRARY" else assert_code_compiles(
        name, "test"
    )

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
