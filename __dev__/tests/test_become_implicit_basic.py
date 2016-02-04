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

        os.mkdir('temp/__dev__')
        touch('temp/__dev__/LICENSE.txt')
        touch('temp/__dev__/tox.ini')
        content = "import setuptools\nsetuptools.setup(name='package')\n"
        touch('temp/__dev__/setup.py', content)
        content = "package"
        touch('temp/__dev__/package_name.txt', content)

        self.backup_cwd = os.getcwd()
        os.chdir('temp')

    def test_become_implicit(self):
        #os.system('tree')
        insideout.main([])
        #os.system('tree')

        ref = ['LICENSE.txt', 'README.md', 'package', 'setup.py', 'tox.ini']
        files = os.listdir('.')
        self.assertTrue(ref == sorted(files))

        ref = ['__init__.py', 'main.py', 'tools.py']
        files = os.listdir('package')
        self.assertTrue(ref == sorted(files))

    def __clean(self):
        try:
            shutil.rmtree('temp')
        except:
            pass

    def tearDown(self):
        os.chdir(self.backup_cwd)
        self.__clean()
