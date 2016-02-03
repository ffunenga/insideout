from __future__ import print_function
import os
import sys
import shutil
import getpass
import setuptools

import insideout


argv = sys.argv[1:]
test_suite = os.environ.get('TOXTESTSUITE', 'tests')


if 'test' in argv:
    pass


if 'clean' in argv:
    shutil.rmtree('%s.egg-info' % insideout.__name__, ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    shutil.rmtree('env', ignore_errors=True)
    def pyclean(path):
        for root, drs, fns in os.walk(path):
            pycache = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache, ignore_errors=True)
            filtered_fns = filter(lambda f: f.endswith('.pyc'), fns)
            for fn in filtered_fns:
                _fn = os.path.join(root, fn)
                os.remove(_fn)
    pyclean(insideout.__name__)
    pyclean('tests')
    shutil.rmtree('.tox', ignore_errors=True)


long_description = """\
A tool to swap the files on your repository's root directory with the ones inside your python package.

    Why aren't the files inside a Python package the first thing we see when we look at its github repository?

Pure Python code (2 and 3 compatible).
"""


setuptools.setup(
    name=insideout.__name__,
    description=insideout.__description__,
    long_description=long_description,
    version=insideout.__version__,
    author='Filipe Funenga',
    author_email='fmafunenga@gmail.com',
    url='https://github.com/ffunenga/%s' % insideout.__name__,
    license=insideout.__license__,
    packages=[insideout.__name__],
    test_suite = test_suite,
    entry_points = {
        'console_scripts' : [
            '{pkg} = {pkg}:main'.format(pkg=insideout.__name__)
        ]
    }
)
