#!/usr/bin/env python
import os
import shutil
import sys
import subprocess
from subprocess import call
import uuid

import unittest


class IntegrationTestActions(unittest.TestCase):
    def setUp(self):
        self.createscript = os.path.abspath(os.path.dirname(__file__)) + '/' + '../bin/create.py'
        self.workspace = os.path.realpath('./') + '/target/'
        shutil.rmtree(self.workspace, True)
        os.mkdir(self.workspace)
        pass

    def runCreate(self, project_prefix, service_type):
        workspace = self.workspace
        process = subprocess.Popen(['python', self.createscript, project_prefix, "--type", service_type],
                                           stderr=subprocess.STDOUT,
                                           stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE,
                                           env=dict(os.environ, WORKSPACE=workspace))

        out, err = process.communicate(input='Y\nn\nY\nn\nY\nY\nn')

        if process.returncode is not 0:
            print (out)
            self.fail(msg="script did not execute correctly, see output for errors")

    def tearDown(self):
        shutil.rmtree(self.workspace)

    def test_created_code_compiles(self):
        workspace = self.workspace
        print('workspace Used : '+ self.workspace)
        project_prefix = "test_project_" + str(uuid.uuid4())

        print project_prefix

        self.runCreate(project_prefix + '-backend', 'BACKEND')
        self.runCreate(project_prefix + '-frontend', 'FRONTEND')
        self.runCreate(project_prefix + '-library', 'LIBRARY')

        projects = [
            workspace + project_prefix + '-backend',
            workspace + project_prefix + '-frontend',
            workspace + project_prefix + '-library']

        for project in projects:
            print('calling compile on ' + project)
            compile_process = subprocess.Popen(['sbt', 'compile'], cwd=project)
            o, e = compile_process.communicate()
            print(str(o))
            print('return code was ' + str(compile_process.returncode))

            if compile_process.returncode is not 0:
                self.fail(msg="project did not compile, see output for errors")

        for project in projects:
            print('calling test on ' + project)
            test_process = subprocess.Popen(['sbt', 'test'], cwd=project)
            o, e = test_process.communicate()
            print(str(o))
            print('return code was ' + str(test_process.returncode))

            if test_process.returncode is not 0:
                self.fail(msg="tests in project failed, see output for errors")



if __name__ == '__main__':
    unittest.main()
