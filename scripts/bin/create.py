#!/usr/bin/env python

import argparse
import distutils.core
import fileinput
import os
import re
import shutil
import subprocess
import sys
from urllib import request as url_request

import pyratemp


def required_environment_directory(environment_variable, description_for_error):
    directory = os.environ.get(environment_variable, None)
    if not directory:
        print(
            f"'{environment_variable}' environment variable is required. You can add this to your ~/.bash_profile by adding the line {environment_variable}=[{description_for_error}]")
        exit(1)
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print(f"Error: '{environment_variable}' environment variable points to non-existent directory: {directory}")
        sys.exit(1)
    return directory


workspace = required_environment_directory("WORKSPACE", "your workspace root dir")


def get_latest_sbt_plugin_version(group, artefact):
    return lookup_latest_artefact_version(group, artefact)


def get_latest_library_version(group, artefact, scala_binary_version):
    latest = lookup_latest_artefact_version(group, artefact + "_" + scala_binary_version)

    if re.search("-play-(\d)*$", latest) and not re.search("-play-28$", latest):
        raise Exception("ERROR: Invalid dependency found '%s'" % latest)
    else:
        return latest


def lookup_latest_artefact_version(group, artefact):
    url = "https://artefacts.tax.service.gov.uk/artifactory/api/search/latestVersion?g=" + group + "&a=" + artefact
    print(url)
    request = url_request.Request(url)
    response = url_request.urlopen(request).read().decode('utf-8')
    print(response)
    return response


def replace_variables_for_app(application_root_name, folder_to_search, application_name, service_type, has_mongo=False):
    scala_version = "2.12.14"
    scala_binary_version = re.sub('\.(\d)*$', '', scala_version)
    print(f"scala_binary_version={scala_binary_version}")
    if service_type == "FRONTEND":
        bootstrap_play_version = get_latest_library_version("uk.gov.hmrc", "bootstrap-frontend-play-28",
                                                            scala_binary_version)
    elif service_type == "BACKEND":
        bootstrap_play_version = get_latest_library_version("uk.gov.hmrc", "bootstrap-backend-play-28",
                                                            scala_binary_version)
    else:
        bootstrap_play_version = ""  # template won't use this

    play_frontend_hmrc_version = get_latest_library_version("uk.gov.hmrc", "play-frontend-hmrc", scala_binary_version)
    play_frontend_govuk_version = get_latest_library_version("uk.gov.hmrc", "play-frontend-govuk", scala_binary_version)
    play_language_version = get_latest_library_version("uk.gov.hmrc", "play-language", scala_binary_version)
    mongo_version = get_latest_library_version("uk.gov.hmrc.mongo", "hmrc-mongo-play-28", scala_binary_version)

    sbt_auto_build = get_latest_sbt_plugin_version("uk.gov.hmrc", "sbt-auto-build")
    sbt_distributables = get_latest_sbt_plugin_version("uk.gov.hmrc", "sbt-distributables")

    print(f"sbt_auto_build {sbt_auto_build}")
    print(f"sbt_distributables {sbt_distributables}")

    for subdir, dirs, files in os.walk(folder_to_search):
        if '.git' in dirs:
            dirs.remove('.git')

        for f in files:
            file_name = os.path.join(subdir, f)
            print(f"templating: {subdir} {f}")
            t = pyratemp.Template(filename=os.path.join(subdir, f))
            file_content = t(UPPER_CASE_APP_NAME=application_name.upper(),
                             UPPER_CASE_APP_NAME_UNDERSCORE_ONLY=application_name.upper().replace("-", "_"),
                             APP_NAME=application_name,
                             APP_PACKAGE_NAME=application_root_name.replace("-", ""),
                             SCALA_VERSION=scala_version,
                             type=service_type,
                             MONGO=has_mongo,
                             bootstrapPlayVersion=bootstrap_play_version,
                             playFrontendHmrcVersion=play_frontend_hmrc_version,
                             playFrontendGovukVersion=play_frontend_govuk_version,
                             playLanguageVersion=play_language_version,
                             mongoVersion=mongo_version,
                             sbt_auto_build=sbt_auto_build,
                             sbt_distributables=sbt_distributables,
                             bashbang="#!/bin/bash",
                             shbang="#!/bin/sh",
                             )
            write_to_file(file_name, file_content)


def write_to_file(f, file_content):
    open_file = open(f, 'w')
    open_file.write(file_content)
    open_file.close()


def replace_in_file(file_to_search, replace_this, with_this):
    for line in fileinput.input(file_to_search, inplace=True):
        print(line.replace(replace_this, with_this)),


def delete_files_for_type(project_folder, service_type):
    file_name = os.path.join(os.path.join(project_folder, "template"), "%s.delete" % service_type)
    for line in fileinput.input(file_name, inplace=False):
        file_name = os.path.join(project_folder, line).strip()
        if os.path.isfile(file_name):
            os.remove(file_name)
        if os.path.isdir(file_name):
            shutil.rmtree(file_name)


def call(command, quiet=True):
    if not quiet:
        print(f"calling: '{command}' from: '{os.getcwd()}'")
    ps_command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ps_command.wait()
    return ps_command


def create_project(project_name, project_type, dry_run, has_mongo, github_token, default_branch):
    if project_type == "LIBRARY":
        template_dir = os.path.normpath(os.path.join(os.path.realpath(__file__), "../../../templates/library"))
        repository_type = "library"
    elif project_type in ["FRONTEND", "BACKEND"]:
        template_dir = os.path.normpath(os.path.join(os.path.realpath(__file__), "../../../templates/service"))
        repository_type = "service"
    else:
        raise Exception("ERROR: Invalid type '%s'" % project_type)

    print(f"project name: {project_name}")

    if not dry_run:
        print(f"Pushing repo '{project_name}'.")
        clone_repo(project_name, github_token)

    print(f"Creating new {repository_type}: {project_name}, this could take a few moments")
    project_folder = os.path.normpath(os.path.join(workspace, project_name))
    add_repository_type(project_folder, repository_type)
    distutils.dir_util.copy_tree(template_dir, project_folder)
    replace_variables_for_app(project_name, project_folder, project_name, project_type, has_mongo)
    if project_type != "LIBRARY":
        delete_files_for_type(project_folder, project_type)
        shutil.rmtree(os.path.join(project_folder, "template"))
        move_folders_to_project_package(project_name, project_folder)
    print(f"Created {project_type} at '{project_folder}'.")
    commit_repo(project_folder, project_name, new_repo=dry_run)

    if not dry_run:
        print(f"Pushing repo '{project_name}'.")
        push_repo(project_name, default_branch)


def move_folders_to_project_package(project_root_name, project_folder):
    project_app_folder = "%s/app" % project_folder
    project_test_folder = "%s/test" % project_folder
    project_it_test_folder = "%s/it" % project_folder
    project_package = "uk/gov/hmrc/%s" % project_root_name.replace("-", "")
    project_package_app = os.path.join(project_app_folder, project_package)
    project_package_test = os.path.join(project_test_folder, project_package)
    project_package_it_test = os.path.join(project_it_test_folder, project_package)

    package_app_dirs = os.listdir(project_app_folder)
    print(package_app_dirs)
    if 'assets' in package_app_dirs:
        package_app_dirs.remove('assets')

    move_files_to_dist(package_app_dirs, project_app_folder, project_package_app)
    move_files_to_dist(os.listdir(project_test_folder), project_test_folder, project_package_test)
    move_files_to_dist(os.listdir(project_it_test_folder), project_it_test_folder, project_package_it_test)


def move_files_to_dist(dirs, src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for d in dirs:
        full_path = src + "/" + d
        shutil.move(full_path, dst)


def add_repository_type(project_folder, repository_type):
    filename = "%s/repository.yaml" % project_folder
    if os.path.exists(filename):
        with open(filename, "a") as f:
            f.write("\ntype: %s" % repository_type)
        f.close()


def clone_repo(repo, github_token):
    command = 'git clone https://%s@github.com/hmrc/%s' % (github_token, repo)
    ps_command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=workspace)
    ps_command.communicate()
    if ps_command.returncode != 0:
        raise Exception("ERROR: Unable to clone repo '%s'" % repo)


def commit_repo(project_folder, project_name, new_repo):
    os.chdir(project_folder)
    if new_repo:
        call('git init')
    call('git add . -A')
    call('git commit -m \"Creating new service %s\"' % project_name)


def push_repo(project_name, default_branch):
    command = f'git push -u origin {default_branch}'
    print(f"pushing repo: {command}")

    fnull = open(os.devnull, 'w')
    ps_command = subprocess.Popen(command, shell=True, stdout=fnull, stderr=fnull, cwd=workspace + '/' + project_name)
    ps_command.communicate()
    if ps_command.returncode != 0:
        raise Exception("ERROR: Unable to push repo '%s'" % project_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Template Creation Tool - Create an new open service(s)... fast!')
    parser.add_argument('REPOSITORY', type=str, help='The name of the service you want to create')
    parser.add_argument('--type', choices=['FRONTEND', 'BACKEND', 'LIBRARY'],
                        help='Sets the type of repository to be either a Play template for FRONTEND or BACKEND microservice or a Play library')
    parser.add_argument('--dry-run', action='store_true',
                        help='Set --dry-run to avoid connecting with remote GitHub repository')
    parser.add_argument('--with-mongo', action='store_true',
                        help='Does your service require Mongo? This only available if the repository is of type "BACKEND"')
    parser.add_argument('--github-token', help='The GitHub token authorised to push to the repository')
    parser.add_argument('--default-branch', default='master',
                        help='The default branch name for the GitHub repository when pushing changes')
    args = parser.parse_args()

    create_project(args.REPOSITORY, args.type, args.dry_run, args.with_mongo, args.github_token, args.default_branch)
