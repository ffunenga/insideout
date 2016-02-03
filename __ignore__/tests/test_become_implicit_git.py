from __future__ import print_function
import unittest
import os
import shutil

import insideout


def touch(path, content='(...)'):
    with open(path, 'w') as f:
        f.write(content)


class TestCase(unittest.TestCase):

    def setUp(self):
        self.__clean()
        os.mkdir('temp')

        touch('temp/README.md')
        touch('temp/__init__.py')
        touch('temp/main.py')
        touch('temp/tools.py')

        os.mkdir('temp/.git')
        os.mkdir('temp/__ignore__')
        touch('temp/__ignore__/LICENSE.txt')
        touch('temp/__ignore__/tox.ini')
        content = "import setuptools\nsetuptools.setup(name='package')\n"
        touch('temp/__ignore__/setup.py', content)
        content = "package"
        touch('temp/__ignore__/package_name.txt', content)

        self.backup_cwd = os.getcwd()
        os.chdir('temp')

    def test_become_implicit(self):
        insideout.main([])
        files = os.listdir('.')
        self.assertTrue('.git' in files)

    def __clean(self):
        try:
            shutil.rmtree('temp')
        except:
            pass

    def tearDown(self):
        os.chdir(self.backup_cwd)
        self.__clean()
