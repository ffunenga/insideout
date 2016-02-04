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

        os.mkdir('temp/subpackage1')
        touch('temp/subpackage1/__init__.py')
        touch('temp/subpackage1/comms.py')

        os.mkdir('temp/subpackage2')
        touch('temp/subpackage2/__init__.py')
        touch('temp/subpackage2/parsers.py')

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

        files = os.listdir('package')
        self.assertTrue('subpackage1' in sorted(files))
        self.assertTrue('subpackage2' in sorted(files))

        files = os.listdir('package/subpackage1')
        self.assertTrue('__init__.py' in sorted(files))
        self.assertTrue('comms.py' in sorted(files))

        files = os.listdir('package/subpackage2')
        self.assertTrue('__init__.py' in sorted(files))
        self.assertTrue('parsers.py' in sorted(files))

    def __clean(self):
        try:
            shutil.rmtree('temp')
        except:
            pass

    def tearDown(self):
        os.chdir(self.backup_cwd)
        self.__clean()
