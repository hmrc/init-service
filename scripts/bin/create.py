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


def get_latest_sbt_plugin_version_in_open(artifact):
    return get_sbt_plugin_version_info_from_bintray(artifact)


def get_latest_library_version_in_open(artifact, scalaVersion="_2.11"):
    artifact_with_version = artifact + scalaVersion
    maven_metadata = get_library_version_info_from_bintray(artifact_with_version)

    try:
        data = maven_metadata.getElementsByTagName("versioning")[0]
    except:
        print "Unable to get latest version from bintray"
        return None

    return data.getElementsByTagName("latest")[0].firstChild.nodeValue


def max_version_of(*args):
    def rank(ver):
        ver = ver or ""
        return [int(s) for s in ver.split(".") if s.isdigit()]

    return sorted(args, key=rank, reverse=True)[0]


def find_version_in(dom):
    latest = "latestRelease"
    try:
        data = dom.getElementsByTagName("artifact")[0]
        latestNode = data.getElementsByTagName(latest)[0]
    except:
        return None
    return latestNode.firstChild.nodeValue


def get_library_version_info_from_bintray(artifact):
    return get_maven_version_info_from_bintray("releases", artifact)


def get_sbt_plugin_version_info_from_bintray(artifact):
    return get_ivy_version_info_from_bintray("sbt-plugin-releases", artifact)


def get_ivy_version_info_from_bintray(repository_name, artifact):
    bintray = "https://api.bintray.com/packages/hmrc/" + repository_name + "/" + artifact
    print(bintray)
    request = urllib2.Request(bintray)
    response = urllib2.urlopen(request).read()
    return json.loads(response)['latest_version']


def get_maven_version_info_from_bintray(repository_name, artifact):
    bintray = "https://dl.bintray.com/hmrc/" + repository_name + "/uk/gov/hmrc/" + artifact + "/maven-metadata.xml"
    print(bintray)
    request = urllib2.Request(bintray)
    response = urllib2.urlopen(request)
    dom = parse(response)
    response.close()
    return dom


def lookup_credentials():
    sbt_credentials = os.environ["HOME"] + "/.sbt/.credentials"
    if not os.path.exists(sbt_credentials):
        print "Cannot look up nexus credentials from " + sbt_credentials
        return {}
    return {key.strip(): value.strip() for (key, value) in
            map(lambda x: x.split("=", 1), open(sbt_credentials, 'r').readlines())}


def _header_credentials():
    credentials = lookup_credentials()
    return credentials["user"] + ":" + credentials["password"]


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


def generate_app_secret():
    lst = [random.choice(string.ascii_letters + string.digits) for n in xrange(64)]
    application_secret = ''.join(lst)
    return application_secret


def replace_variables_for_app(application_root_name, folder_to_search, application_name, service_type, has_mongo=False):
    govukTemplateVersion = get_latest_library_version_in_open("govuk-template")
    frontendBootstrapVersion = get_latest_library_version_in_open("frontend-bootstrap")
    playUiVersion = get_latest_library_version_in_open("play-ui")
    playPartialsVersion = get_latest_library_version_in_open("play-partials")
    playAuthVersion = get_latest_library_version_in_open("play-authorisation")
    playAuthorisedFrontendVersion = get_latest_library_version_in_open("play-authorised-frontend")
    microserviceBootstrapVersion = get_latest_library_version_in_open("microservice-bootstrap")
    playUrlBindersVersion = get_latest_library_version_in_open("play-url-binders")
    playConfigVersion = get_latest_library_version_in_open("play-config")
    domainVersion = get_latest_library_version_in_open("domain")
    hmrcTestVersion = get_latest_library_version_in_open("hmrctest")
    playReactivemongoVersion = get_latest_library_version_in_open("play-reactivemongo")
    simpleReactivemongoVersion = get_latest_library_version_in_open("simple-reactivemongo")
    playHealthVersion = get_latest_library_version_in_open("play-health")
    logbackJsonLoggerVersion = get_latest_library_version_in_open("logback-json-logger")

    sbt_auto_build = get_latest_sbt_plugin_version_in_open("sbt-auto-build")
    sbt_git_versioning = get_latest_sbt_plugin_version_in_open("sbt-git-versioning")
    sbt_distributables = get_latest_sbt_plugin_version_in_open("sbt-distributables")

    print("sbt_auto_build  " + sbt_auto_build)
    print("sbt_git_versioning  " + sbt_git_versioning)
    print("sbt_distributables  " + sbt_distributables)

    for subdir, dirs, files in os.walk(folder_to_search):
        if '.git' in dirs:
            dirs.remove('.git')

        for f in files:
            file_name = os.path.join(subdir, f)
            t = pyratemp.Template(filename=os.path.join(subdir, f))
            file_content = t(UPPER_CASE_APP_NAME=application_name.upper(),
                             UPPER_CASE_APP_NAME_UNDERSCORE_ONLY=application_name.upper().replace("-", "_"),
                             APP_NAME=application_name,
                             APP_PACKAGE_NAME=application_root_name.replace("-", ""),
                             SECRET_KEY=generate_app_secret(),
                             type=service_type,
                             MONGO=has_mongo,
                             govukTemplateVersion=govukTemplateVersion,
                             microserviceBootstrapVersion=microserviceBootstrapVersion,
                             playUrlBindersVersion=playUrlBindersVersion,
                             playConfigVersion=playConfigVersion,
                             domainVersion=domainVersion,
                             hmrcTestVersion=hmrcTestVersion,
                             frontendBootstrapVersion=frontendBootstrapVersion,
                             playUiVersion=playUiVersion,
                             playAuthVersion=playAuthVersion,
                             playPartialsVersion=playPartialsVersion,
                             playAuthorisedFrontendVersion=playAuthorisedFrontendVersion,
                             playReactivemongoVersion=playReactivemongoVersion,
                             simpleReactivemongoVersion=simpleReactivemongoVersion,
                             playHealthVersion=playHealthVersion,
                             logbackJsonLoggerVersion=logbackJsonLoggerVersion,
                             sbt_auto_build=sbt_auto_build,
                             sbt_git_versioning=sbt_git_versioning,
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


def clone_git_repo(repo, folder):
    os.chdir(folder)
    call('git clone %s' % repo)

def add_mongo_to_travis(project_folder, existing_repo, has_mongo=False):
    if has_mongo and existing_repo:
        file_name = os.path.join(project_folder, ".travis.yml")

        fh = open(file_name, "a")

        travis_mongo_config = \
            ("services:\n"
             "- mongodb\n"
             "addons:\n"
             "  apt:\n"
             "    sources:\n"
             "    - mongodb-3.0-precise\n"
             "    packages:\n"
             "    - mongodb-org-server\n")

        fh.writelines(travis_mongo_config)
        fh.close()

def create_service(project_root_name, service_type, existing_repo, has_mongo=False):
    project_name = folder_name(project_root_name, service_type)
    template_dir = os.path.normpath(os.path.join(os.path.realpath(__file__), "../../../templates/service"))

    print("project name :" + project_name)

    if existing_repo:
        clone_repo(project_name)

    print "Creating new service: %s, this could take a few moments" % project_name
    project_folder = os.path.normpath(os.path.join(workspace, project_name))
    if os.path.isdir(project_folder) and not existing_repo:
        print "The folder '%s' already exists, not creating front end module" % str(project_folder)
    else:
        distutils.dir_util.copy_tree(template_dir, project_folder)
        replace_variables_for_app(project_root_name, project_folder, project_name, service_type, has_mongo)
        delete_files_for_type(project_folder, service_type)
        shutil.rmtree(os.path.join(project_folder, "template"))
        move_folders_to_project_package(project_root_name, project_folder, service_type)
        add_mongo_to_travis(project_folder, existing_repo, has_mongo)
        print "Created %s at '%s'." % (
            service_type, project_folder)
        print "Pushing repo '%s'." % project_folder
        commit_repo(project_folder, project_name)
        push_repo(project_name)


def move_folders_to_project_package(project_root_name, project_folder, service_type):
    project_app_folder = "%s/app" % project_folder
    project_test_folder = "%s/test" % project_folder
    project_package = "uk/gov/hmrc/%s" % project_root_name.replace("-", "")
    project_package_app = os.path.join(project_app_folder, project_package)
    project_package_test = os.path.join(project_test_folder, project_package)

    move_files_to_dist(os.listdir(project_app_folder), project_app_folder, project_package_app)
    move_files_to_dist(os.listdir(project_test_folder), project_test_folder, project_package_test)


def move_files_to_dist(files, src, dst):
    for f in files:
        full_path = src + "/" + f
        shutil.move(full_path, dst)


def folder_name(project_name, project_type):
    folder_name = project_name
    if project_type == "FRONTEND":
        folder_name = "%s-frontend" % project_name
    if project_type == "STUB":
        folder_name = "%s-stub" % project_name
    return folder_name


def clone_repo(repo):
    command = 'git clone git@github.com:hmrc/%s.git' % repo
    print("cloning : " + command)
    ps_command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=workspace)
    ps_command.communicate()
    if ps_command.returncode is not 0:
        print "ERROR: Unable to clone repo '%s'" % repo


def commit_repo(project_folder, project_name):
    os.chdir(project_folder)
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
    parser.add_argument('PROJECT_NAME', type=str, help='The name of the project you want to create')
    parser.add_argument('TYPE', choices=['FRONTEND', 'MICROSERVICE'], help='Sets the type of repository to be either a Play template for FRONTEND or MICROSERVICE')
    parser.add_argument('-exists', action='store_true', help='Does the repository already exists?')
    parser.add_argument('-use_mongo', action='store_true', help='Does your service require Mongo? This only available if the repository is of type "MICROSERVICE"')
    args = parser.parse_args()

    if args.TYPE == 'MICROSERVICE':
        create_service(args.PROJECT_NAME, args.TYPE, args.exists, args.use_mongo)
    elif args.TYPE == 'FRONTEND':
        create_service(args.PROJECT_NAME, args.TYPE, args.exists)