#!/usr/bin/env python

import distutils.core
import fileinput
import os
import re
import shutil
import subprocess
import sys
from urllib import request as url_request

import init_service.pyratemp as pyratemp


class InitService:
    def __init__(self, repository, type, dry_run, github_token, with_mongo, default_branch):
        self.repository = repository
        self.type = type
        self.dry_run = dry_run
        self.github_token = github_token
        self.with_mongo = with_mongo
        self.default_branch = default_branch
        self.workspace = self.required_environment_directory("WORKSPACE", "your workspace root dir")

    def required_environment_directory(self, environment_variable, description_for_error):
        directory = os.environ.get(environment_variable, None)
        if not directory:
            print(
                f"'{environment_variable}' environment variable is required. You can add this to your ~/.bash_profile by adding the line {environment_variable}=[{description_for_error}]"
            )
            exit(1)
        directory = os.path.abspath(directory)
        if not os.path.isdir(directory):
            print(
                f"Error: '{environment_variable}' environment variable points to non-existent directory: {directory}"
            )
            sys.exit(1)
        return directory

    def get_latest_sbt_plugin_version(self, group, artefact):
        return self.lookup_latest_artefact_version(group, artefact)

    def get_latest_library_version(self, group, artefact, scala_binary_version):
        latest = self.lookup_latest_artefact_version(group, artefact + "_" + scala_binary_version)

        if re.search(r"-play-(\d)*$", latest) and not re.search("-play-28$", latest):
            raise Exception("ERROR: Invalid dependency found '%s'" % latest)
        else:
            return latest

    def lookup_latest_artefact_version(self, group, artefact):
        artifactory_uri = os.getenv(
            "ARTIFACTORY_URI", "https://artefacts.tax.service.gov.uk/artifactory"
        )
        url = artifactory_uri + "/api/search/latestVersion?g=" + group + "&a=" + artefact
        print(url)
        request = url_request.Request(url)
        response = url_request.urlopen(request).read().decode("utf-8")
        print(response)
        return response

    def replace_variables_for_app(self, folder_to_search):
        sbt_version = "1.7.2"
        scala_version = "2.13.8"
        scala_binary_version = re.sub(r"\.(\d)*$", "", scala_version)
        print(f"scala_binary_version={scala_binary_version}")
        if self.type == "FRONTEND":
            bootstrap_play_version = self.get_latest_library_version(
                "uk.gov.hmrc", "bootstrap-frontend-play-28", scala_binary_version
            )
        elif self.type == "BACKEND":
            bootstrap_play_version = self.get_latest_library_version(
                "uk.gov.hmrc", "bootstrap-backend-play-28", scala_binary_version
            )
        else:
            bootstrap_play_version = ""  # template won't use this

        play_frontend_hmrc_version = self.get_latest_library_version(
            "uk.gov.hmrc", "play-frontend-hmrc", scala_binary_version
        )
        play_language_version = self.get_latest_library_version(
            "uk.gov.hmrc", "play-language", scala_binary_version
        )
        mongo_version = self.get_latest_library_version(
            "uk.gov.hmrc.mongo", "hmrc-mongo-play-28", scala_binary_version
        )

        sbt_auto_build = self.get_latest_sbt_plugin_version("uk.gov.hmrc", "sbt-auto-build")
        sbt_distributables = self.get_latest_sbt_plugin_version("uk.gov.hmrc", "sbt-distributables")

        print(f"sbt_auto_build {sbt_auto_build}")
        print(f"sbt_distributables {sbt_distributables}")

        for subdir, dirs, files in os.walk(folder_to_search):
            if ".git" in dirs:
                dirs.remove(".git")

            for f in files:
                file_name = os.path.join(subdir, f)
                print(f"templating: {subdir} {f}")
                t = pyratemp.Template(filename=os.path.join(subdir, f))
                file_content = t(
                    UPPER_CASE_APP_NAME=self.repository.upper(),
                    UPPER_CASE_APP_NAME_UNDERSCORE_ONLY=self.repository.upper().replace("-", "_"),
                    APP_NAME=self.repository,
                    APP_PACKAGE_NAME=self.repository.replace("-", ""),
                    SBT_VERSION=sbt_version,
                    SCALA_VERSION=scala_version,
                    type=self.type,
                    MONGO=self.with_mongo,
                    bootstrapPlayVersion=bootstrap_play_version,
                    playFrontendHmrcVersion=play_frontend_hmrc_version,
                    playLanguageVersion=play_language_version,
                    mongoVersion=mongo_version,
                    sbt_auto_build=sbt_auto_build,
                    sbt_distributables=sbt_distributables,
                    bashbang="#!/bin/bash",
                    shbang="#!/bin/sh",
                )
                self.write_to_file(file_name, file_content)

    def write_to_file(self, f, file_content):
        open_file = open(f, "w")
        open_file.write(file_content)
        open_file.close()

    def replace_in_file(self, file_to_search, replace_this, with_this):
        for line in fileinput.input(file_to_search, inplace=True):
            print(line.replace(replace_this, with_this)),

    def delete_files_for_type(self, project_folder):
        file_name = os.path.join(os.path.join(project_folder, "template"), f"{self.type}.delete")
        for line in fileinput.input(file_name, inplace=False):
            file_name = os.path.join(project_folder, line).strip()
            if os.path.isfile(file_name):
                os.remove(file_name)
            if os.path.isdir(file_name):
                shutil.rmtree(file_name)

    def call(self, command, quiet=True):
        if not quiet:
            print(f"calling: '{command}' from: '{os.getcwd()}'")
        ps_command = subprocess.Popen(
            command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        ps_command.wait()
        return ps_command

    def create_project(self):
        if self.type == "LIBRARY":
            template_dir = os.path.normpath(
                os.path.join(os.path.abspath(__file__), "../templates/library")
            )
            repository_type = "library"
        elif self.type in ["FRONTEND", "BACKEND"]:
            template_dir = os.path.normpath(
                os.path.join(os.path.abspath(__file__), "../templates/service")
            )
            repository_type = "service"
        else:
            raise Exception(f"ERROR: Invalid type '{self.type}'")

        print(f"project name: {self.repository}")

        if not self.dry_run:
            print(f"Cloning repo '{self.repository}'.")
            self.clone_repo()

        print(f"Creating new {repository_type}: {self.repository}, this could take a few moments")
        project_folder = os.path.normpath(os.path.join(self.workspace, self.repository))
        self.add_repository_type(project_folder, repository_type)
        distutils.dir_util.copy_tree(template_dir, project_folder)
        self.replace_variables_for_app(project_folder)
        if self.type != "LIBRARY":
            self.delete_files_for_type(project_folder)
            shutil.rmtree(os.path.join(project_folder, "template"))
            self.move_folders_to_project_package(project_folder)
        print(f"Created {self.type} at '{project_folder}'.")
        self.commit_repo(project_folder)

        if not self.dry_run:
            print(f"Pushing repo '{self.repository}'.")
            self.push_repo()

    def move_folders_to_project_package(self, project_folder):
        project_app_folder = f"{project_folder}/app"
        project_test_folder = f"{project_folder}/test"
        project_it_test_folder = f"{project_folder}/it"
        project_package = f"uk/gov/hmrc/{self.repository.replace('-', '')}"
        project_package_app = os.path.join(project_app_folder, project_package)
        project_package_test = os.path.join(project_test_folder, project_package)
        project_package_it_test = os.path.join(project_it_test_folder, project_package)

        package_app_dirs = os.listdir(project_app_folder)
        print(package_app_dirs)
        if "assets" in package_app_dirs:
            package_app_dirs.remove("assets")

        self.move_files_to_dist(package_app_dirs, project_app_folder, project_package_app)
        self.move_files_to_dist(
            os.listdir(project_test_folder), project_test_folder, project_package_test
        )
        self.move_files_to_dist(
            os.listdir(project_it_test_folder), project_it_test_folder, project_package_it_test
        )

    def move_files_to_dist(self, dirs, src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)

        for d in dirs:
            full_path = src + "/" + d
            shutil.move(full_path, dst)

    def add_repository_type(self, project_folder, repository_type):
        filename = f"{project_folder}/repository.yaml"
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write(f"\ntype: {repository_type}")
            f.close()

    def clone_repo(self):
        command = ["git", "clone", f"https://{self.github_token}@github.com/hmrc/{self.repository}"]
        ps_command = subprocess.Popen(
            command, shell=False, stdout=subprocess.PIPE, cwd=self.workspace
        )
        ps_command.communicate()
        if ps_command.returncode != 0:
            raise Exception(f"ERROR: Unable to clone repo '{self.repository}'")

    def commit_repo(self, project_folder):
        os.chdir(project_folder)
        if self.dry_run:
            self.call(["git", "init"])
        self.call(["git", "add", ".", "-A"])
        self.call(["git", "commit", "-m", f"'Creating new service {self.repository}'"])

    def push_repo(self):
        command = ["git", "push", "-u", "origin", self.default_branch]
        print(f"pushing repo: {command}")
        fnull = open(os.devnull, "w")
        ps_command = subprocess.Popen(
            command,
            shell=False,
            stdout=fnull,
            stderr=fnull,
            cwd=self.workspace + "/" + self.repository,
        )
        ps_command.communicate()
        if ps_command.returncode != 0:
            raise Exception(f"ERROR: Unable to push repo '{self.repository}'")
