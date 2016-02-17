from __future__ import print_function
import os
import shutil
import sys
import setuptools


PACKAGE_NAME = 'insideout'


# ---------------------------------------------------------------------------- #
#
# The following segment of code enables this setup.py to work as expected
# from anywhere.
#
# From the root of the repository you can run these:
#     $ python __dev__/setup.py install
#     $ tox -c __dev__/tox.ini
#
# From inside __dev__ you can run these:
#     $ python setup.py install
#     $ tox
#
# If you organize your code in the classical testing/deployment focused
# structure (where all the test configuration files, license, etc., are placed
# in the root directory of your repository) then this setup.py also works.
# Although, you shouldn't do it. Just look at it: it's ugly.
#
# --- SEGMENT OF CODE -------------------------------------------------------- #

_t = os.path.abspath(__file__)
cwd = os.path.dirname(_t)

if os.path.basename(cwd) == '__dev__':

    os.chdir(cwd)

    shutil.rmtree(PACKAGE_NAME, ignore_errors=True)
    ignore_list = shutil.ignore_patterns('__dev__*', '.git*', 'env*', '.tox')
    shutil.copytree('..', PACKAGE_NAME, ignore=ignore_list)

# --- END OF SEGMENT OF CODE ------------------------------------------------- #


def rmdir(dname):
    shutil.rmtree(os.path.join('..', dname), ignore_errors=True)
    shutil.rmtree(dname, ignore_errors=True)


if 'reset' in sys.argv[1:]:
    rmdir('env')
    sys.argv = [('clean' if a == 'reset' else a) for a in sys.argv]


if 'clean' in sys.argv[1:]:
    shutil.rmtree(PACKAGE_NAME, ignore_errors=True)
    rmdir('%s.egg-info' % PACKAGE_NAME)
    rmdir('build')
    rmdir('dist')
    rmdir('.tox')
    rmdir('.cache')
    rmdir('.eggs')
    for root, drs, fns in os.walk('.'):
        pycache = os.path.join(root, '__pycache__')
        shutil.rmtree(pycache, ignore_errors=True)
        filtered_fns = filter(lambda f: f.endswith('.pyc'), fns)
        for fn in filtered_fns:
            _fn = os.path.join(root, fn)
            os.remove(_fn)
    sys.exit()


def get_long_description(fname='README.md'):
    try:
        with open(fname) as f:
            content = f.read()
    except:
        content = ''
    else:
        ini = content.find('Why')
        end = content.find('repository.')
        end += len('repository.')
        content = content[ini:end]
    return content


package = __import__(PACKAGE_NAME)


setuptools.setup(
    name=package.__name__,
    description=package.__description__,
    long_description=get_long_description(),
    version=package.__version__,
    author='Filipe Funenga',
    author_email='fmafunenga@gmail.com',
    url='https://github.com/ffunenga/%s' % package.__name__,
    license=package.__license__,
    packages=[package.__name__],
    test_suite = os.environ.get('TOXTESTSUITE', 'tests'),
    entry_points = {
        'console_scripts' : [
            '{pkg} = {pkg}:main'.format(pkg=package.__name__)
        ]
    }
)
