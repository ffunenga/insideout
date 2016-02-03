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
        touch('temp/LICENSE.txt')
        touch('temp/tox.ini')
        content = "import setuptools\nsetuptools.setup(name='package')\n"
        touch('temp/setup.py', content)

        os.mkdir('temp/package')
        touch('temp/package/__init__.py')
        touch('temp/package/main.py')
        touch('temp/package/tools.py')

        os.mkdir('temp/package/subpackage1')
        touch('temp/package/subpackage1/__init__.py')
        touch('temp/package/subpackage1/comms.py')

        os.mkdir('temp/package/subpackage2')
        touch('temp/package/subpackage2/__init__.py')
        touch('temp/package/subpackage2/parsers.py')


        self.backup_cwd = os.getcwd()
        os.chdir('temp')

    def test_become_explicit(self):
        insideout.main([])

        files = os.listdir('.')
        self.assertTrue('subpackage1' in sorted(files))
        self.assertTrue('subpackage2' in sorted(files))

        files = os.listdir('subpackage1')
        self.assertTrue('__init__.py' in sorted(files))
        self.assertTrue('comms.py' in sorted(files))

        files = os.listdir('subpackage2')
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
