#!/usr/bin/env python

import sys
import argparse
import os
import distutils.core
import string
import random
import subprocess
import fileinput
import shutil
import pyratemp
import urllib2
import json
from xml.dom.minidom import parse
import re


def required_environment_directory(environment_variable, description_for_error):
    directory = os.environ.get(environment_variable, None)
    if not directory:
        print "'%s' environment variable is required. You can add this to your ~/.bash_profile by adding the line %s=[%s]" % (
            environment_variable, environment_variable, description_for_error)
        exit(1)
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
        print "Error: '%s' environment variable points to non-existent directory: %s" % (
            environment_variable, directory)
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
        return latest.replace("-play-28", "-play-27")

def lookup_latest_artefact_version(group, artefact):
    url = "https://artefacts.tax.service.gov.uk/artifactory/api/search/latestVersion?g=" + group + "&a=" + artefact
    print(url)
    request = urllib2.Request(url)
    response = urllib2.urlopen(request).read().decode('utf-8')
    print(response)
    return response


def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def replace_variables_for_app(application_root_name, folder_to_search, application_name, service_type, has_mongo=False):
    scalaVersion = "2.12.13"
    scalaBinaryVersion = re.sub('\.(\d)*$', '', scalaVersion)
    print("scalaBinaryVersion=" + scalaBinaryVersion)
    if service_type == "FRONTEND":
        bootstrapPlay27Version = get_latest_library_version("uk.gov.hmrc", "bootstrap-frontend-play-27", scalaBinaryVersion)
    elif service_type == "BACKEND":
        bootstrapPlay27Version = get_latest_library_version("uk.gov.hmrc", "bootstrap-backend-play-27", scalaBinaryVersion)
    else:
        bootstrapPlay27Version="" # template won't use this

    playFrontendHmrcVersion=get_latest_library_version("uk.gov.hmrc", "play-frontend-hmrc", scalaBinaryVersion)
    playFrontendGovukVersion=get_latest_library_version("uk.gov.hmrc", "play-frontend-govuk", scalaBinaryVersion)
    playLanguageVersion=get_latest_library_version("uk.gov.hmrc", "play-language", scalaBinaryVersion)
    mongoVersion=get_latest_library_version("uk.gov.hmrc.mongo", "hmrc-mongo-play-27", scalaBinaryVersion)

    sbt_auto_build = get_latest_sbt_plugin_version("uk.gov.hmrc", "sbt-auto-build")
    sbt_git_versioning = get_latest_sbt_plugin_version("uk.gov.hmrc", "sbt-git-versioning")
    sbt_artifactory = get_latest_sbt_plugin_version("uk.gov.hmrc", "sbt-artifactory")
    sbt_distributables = get_latest_sbt_plugin_version("uk.gov.hmrc", "sbt-distributables")

    print("sbt_auto_build  " + sbt_auto_build)
    print("sbt_git_versioning  " + sbt_git_versioning)
    print("sbt_distributables  " + sbt_distributables)
    print("sbt_artifactory  " + sbt_artifactory)

    for subdir, dirs, files in os.walk(folder_to_search):
        if '.git' in dirs:
            dirs.remove('.git')

        for f in files:
            file_name = os.path.join(subdir, f)
            print("templating: " + subdir + " " + f)
            t = pyratemp.Template(filename=os.path.join(subdir, f))
            file_content = t(UPPER_CASE_APP_NAME=application_name.upper(),
                             UPPER_CASE_APP_NAME_UNDERSCORE_ONLY=application_name.upper().replace("-", "_"),
                             APP_NAME=application_name,
                             APP_PACKAGE_NAME=application_root_name.replace("-", ""),
                             SCALA_VERSION=scalaVersion,
                             type=service_type,
                             MONGO=has_mongo,
                             bootstrapPlay27Version = bootstrapPlay27Version,
                             playFrontendHmrcVersion=playFrontendHmrcVersion,
                             playFrontendGovukVersion=playFrontendGovukVersion,
                             playLanguageVersion=playLanguageVersion,
                             mongoVersion=mongoVersion,
                             sbt_auto_build=sbt_auto_build,
                             sbt_git_versioning=sbt_git_versioning,
                             sbt_distributables=sbt_distributables,
                             sbt_artifactory=sbt_artifactory,
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
        print line.replace(replace_this, with_this),


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
        print "calling: '" + command + "' from: '" + os.getcwd() + "'"
    ps_command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ps_command.wait()
    return ps_command


def create_service(project_name, service_type, existing_repo, has_mongo, github_token):
    if service_type == "LIBRARY":
        template_dir = os.path.normpath(os.path.join(os.path.realpath(__file__), "../../../templates/library"))
    elif service_type in ["FRONTEND", "BACKEND"]:
        template_dir = os.path.normpath(os.path.join(os.path.realpath(__file__), "../../../templates/service"))
    else:
        raise Exception("ERROR: Invalid type '%s'" % service_type)

    print("project name :" + project_name)

    if existing_repo:
        clone_repo(project_name, github_token)

    print "Creating new service: %s, this could take a few moments" % project_name
    project_folder = os.path.normpath(os.path.join(workspace, project_name))
    if os.path.isdir(project_folder) and not existing_repo:
        print "The folder '%s' already exists, not creating front end module" % str(project_folder)
    else:
        distutils.dir_util.copy_tree(template_dir, project_folder)
        replace_variables_for_app(project_name, project_folder, project_name, service_type, has_mongo)
        if service_type != "LIBRARY":
            delete_files_for_type(project_folder, service_type)
            shutil.rmtree(os.path.join(project_folder, "template"))
            move_folders_to_project_package(project_name, project_folder)
        print "Created %s at '%s'." % (service_type, project_folder)
        commit_repo(project_folder, project_name, existing_repo)
        if existing_repo:
            print "Pushing repo '%s'." % project_folder
            push_repo(project_name)


def move_folders_to_project_package(project_root_name, project_folder):
    project_app_folder = "%s/app" % project_folder
    project_test_folder = "%s/test" % project_folder
    project_package = "uk/gov/hmrc/%s" % project_root_name.replace("-", "")
    project_package_app = os.path.join(project_app_folder, project_package)
    project_package_test = os.path.join(project_test_folder, project_package)

    package_app_dirs = os.listdir(project_app_folder)
    print package_app_dirs
    if 'assets' in package_app_dirs:
        package_app_dirs.remove('assets')

    move_files_to_dist(package_app_dirs, project_app_folder, project_package_app)
    move_files_to_dist(os.listdir(project_test_folder), project_test_folder, project_package_test)

def move_files_to_dist(dirs, src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)

    for d in dirs:
        full_path = src + "/" + d
        shutil.move(full_path, dst)


def clone_repo(repo, github_token):
    command = 'git clone https://%s@github.com/hmrc/%s' % (github_token, repo)
    print("cloning : " + command)
    ps_command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=workspace)
    ps_command.communicate()
    if ps_command.returncode is not 0:
        raise Exception("ERROR: Unable to clone repo '%s'" % repo)


def commit_repo(project_folder, project_name, existing_repo):
    os.chdir(project_folder)
    if not existing_repo:
        call('git init')
    call('git add . -A')
    call('git commit -m \"Creating new service %s\"' % project_name)

FNULL = open(os.devnull, 'w')

def push_repo(project_name):
    command = 'git push -u origin master'
    print("pushing repo : " + command)

    ps_command = subprocess.Popen(command, shell=True, stdout=FNULL, stderr=FNULL, cwd=workspace+'/'+project_name)
    ps_command.communicate()
    if ps_command.returncode is not 0:
        raise Exception("ERROR: Unable to push repo '%s'" % project_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Template Creation Tool - Create an new open service(s)... fast!')
    parser.add_argument('REPOSITORY', type=str, help='The name of the service you want to create')
    parser.add_argument('--type', choices=['FRONTEND', 'BACKEND', 'LIBRARY'], help='Sets the type of repository to be either a Play template for FRONTEND or BACKEND microservice or a Play library')
    parser.add_argument('--github-token', help='The github token authorised to push to the repository')
    parser.add_argument('--github', action='store_true', help='Does the repository already exists on github? Set --github for this repo to be cloned, and updated')
    parser.add_argument('--with-mongo', action='store_true', help='Does your service require Mongo? This only available if the repository is of type "BACKEND"')
    args = parser.parse_args()

    create_service(args.REPOSITORY, args.type, args.github, args.with_mongo, args.github_token)
