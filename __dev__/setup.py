from __future__ import print_function
import os
import shutil
import sys
import setuptools


# Change the CWD to __dev__
_t = os.path.abspath(__file__)
cwd = os.path.dirname(_t)
os.chdir(cwd)


# Grabs package name from the root folder
_t = os.path.join(cwd, '..')
_t = os.path.abspath(_t)
package = os.path.basename(_t)


argv = sys.argv[1:]


if 'clean' in argv:
    shutil.rmtree(package, ignore_errors=True)
    shutil.rmtree('%s.egg-info' % package, ignore_errors=True)
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
    #shutil.rmtree('env', ignore_errors=True)
    #shutil.rmtree('.tox', ignore_errors=True)
    sys.exit()


# Replicates package inside __dev__
shutil.rmtree(package, ignore_errors=True)
ignore_list = shutil.ignore_patterns('__dev__*', '.git*')
shutil.copytree('..', package, ignore=ignore_list)


import insideout


if 'test' in argv:
    pass


setuptools.setup(
    name=insideout.__name__,
    description=insideout.__description__,
    long_description=insideout.__lead__,
    version=insideout.__version__,
    author='Filipe Funenga',
    author_email='fmafunenga@gmail.com',
    url='https://github.com/ffunenga/%s' % insideout.__name__,
    license=insideout.__license__,
    packages=[insideout.__name__],
    package_dir={'': '..'},
    test_suite = os.environ.get('TOXTESTSUITE', 'tests'),
    entry_points = {
        'console_scripts' : [
            '{pkg} = {pkg}:main'.format(pkg=insideout.__name__)
        ]
    }
)
