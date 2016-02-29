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
        workspace = os.path.realpath('./') + '/target/'
        os.mkdir(workspace)
        self.workspace = workspace
        pass

    def tearDown(self):
        shutil.rmtree(self.workspace)

    def test_created_code_compiles(self):
        workspace = self.workspace
        print('workspace Used : '+ self.workspace)
        project_prefix = "test_project_" + str(uuid.uuid4())

        print project_prefix

        process = subprocess.Popen(['python', self.createscript, project_prefix],
                                   stderr=subprocess.STDOUT,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   env=dict(os.environ, WORKSPACE=workspace))

        out, err = process.communicate(input='Y\nY\nY\nY')

        if process.returncode is not 0:
            print (out)
            self.fail(msg="script did not execute correctly, see output for errors")

        projects_to_compile = [
            workspace + project_prefix,
            workspace + project_prefix + '-stub',
            workspace + project_prefix + '-frontend']

        for project in projects_to_compile:
            print('calling compile on ' + project)
            compile_process = subprocess.Popen(['sbt', 'compile'], cwd=project)
            o, e = compile_process.communicate()
            print(str(o))
            print('return code was ' + str(process.returncode))

            if process.returncode is not 0:
                self.fail(msg="project did not compile, see output for errors")


if __name__ == '__main__':
    unittest.main()
