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
        os.mkdir('temp/package')
        touch('temp/README.md')
        touch('temp/LICENSE.txt')
        touch('temp/tox.ini')
        touch('temp/package/__init__.py')
        touch('temp/package/main.py')
        touch('temp/package/tools.py')
        content = "import setuptools\nsetuptools.setup(name='package')\n"
        touch('temp/setup.py', content)
        self.backup_cwd = os.getcwd()
        os.chdir('temp')

    def test_become_explicit(self):
        insideout.main([])

        ref = ['README.md', '__ignore__', '__init__.py', 'main.py', 'tools.py']
        files = os.listdir('.')
        self.assertTrue(ref == sorted(files))

        ref = ['LICENSE.txt', 'package_name.txt', 'setup.py', 'tox.ini']
        files = os.listdir('__ignore__')
        self.assertTrue(ref == sorted(files))

        self.assertTrue(os.path.exists('__ignore__/package_name.txt'))
        self.assertTrue(os.path.isfile('__ignore__/package_name.txt'))
        with open('__ignore__/package_name.txt') as f:
            content = f.read().strip()
        self.assertTrue(content == 'package')

    def __clean(self):
        try:
            shutil.rmtree('temp')
        except:
            pass

    def tearDown(self):
        os.chdir(self.backup_cwd)
        self.__clean()
