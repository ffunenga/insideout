from __future__ import print_function
import sys
import os
import shutil
import subprocess


class Config:
    """Sets configuration values for insideout"""

    IGNORE_PATH = '__ignore__'
    PKGNAME_FNAME = 'package_name.txt'


class Tools:
    """Reusable tools for insideout"""

    @staticmethod
    def filter_readme(files):
        readme = None
        _readmes = [f for f in files if f.lower().startswith('readme.')]
        if _readmes:
            _gen = (f for f in _readmes if f.lower() == 'readme.md')
            readme = next(_gen, _readmes[0])
        return readme

    @staticmethod
    class OnErrorMsg:

        def __init__(self, msg):
            self.msg = msg

        def __enter__(self):
            pass

        def __exit__(self, type, value, traceback):
            if value:
                _err_msg = 'Error: %s - %s' % (self.msg, str(value))
                sys.exit(_err_msg)

    @staticmethod
    class TemporaryCWD:

        def __init__(self, path):
            self.path = path

        def __enter__(self):
            self.backup_cwd = os.getcwd()
            os.chdir(self.path)

        def __exit__(self, type, value, traceback):
            os.chdir(self.backup_cwd)
            if value:
                raise


def become_explicit():
    with Tools.OnErrorMsg('failed to retrieve package name'):
        _cmd = ['python', '-B', 'setup.py', '--name']
        pkgname = subprocess.check_output(_cmd, stderr=subprocess.PIPE)
        pkgname = pkgname.decode('utf-8').strip()

    if not (os.path.exists(pkgname) and os.path.isdir(pkgname)):
        sys.exit('package "%s" folder does not exist' % pkgname)

    _err_msg = 'failed to mkdir "%s"' % Config.IGNORE_PATH
    with Tools.OnErrorMsg(_err_msg):
        os.mkdir(Config.IGNORE_PATH)

    with Tools.OnErrorMsg('failed to backup package name'):
        _target = os.path.join(Config.IGNORE_PATH, Config.PKGNAME_FNAME)
        with open(_target, 'w') as f:
            f.write(pkgname)

    files = list(os.listdir('.'))
    readme = Tools.filter_readme(files)
    ignore_list = [Config.IGNORE_PATH, pkgname, readme, '.git']
    _err_fmt = 'failed to hide residual entry "%s" in "%s"'
    for source in files:
        if source not in ignore_list:
            _target = os.path.join(Config.IGNORE_PATH, source)
            _err_msg = _err_fmt % (source, Config.IGNORE_PATH)
            with Tools.OnErrorMsg(_err_msg):
                shutil.move(source, _target)

    _err_fmt = 'failed to move package entry "%s" to root path'
    with Tools.TemporaryCWD(pkgname):
        for source in os.listdir('.'):
            _target = os.path.join('..', source)
            _err_msg = _err_fmt % os.path.join(pkgname, source)
            with Tools.OnErrorMsg(_err_msg):
                shutil.move(source, _target)

    _err_fmt = 'failed to remove package folder "%s"'
    _err_msg = _err_fmt % pkgname
    with Tools.OnErrorMsg(_err_msg):
        shutil.rmtree(pkgname)


def become_implicit():
    _fname = os.path.join(Config.IGNORE_PATH, Config.PKGNAME_FNAME)

    if not (os.path.exists(_fname) and os.path.isfile(_fname)):
        sys.exit('package name file "%s" does not exist' % _fname)

    with Tools.OnErrorMsg('failed to retrieve package name'):
        with open(_fname) as f:
            pkgname = f.read().strip()

    with Tools.OnErrorMsg('failed to mkdir "%s"' % pkgname):
        os.mkdir(pkgname)

    files = list(os.listdir('.'))
    readme = Tools.filter_readme(files)
    ignore_list = [Config.IGNORE_PATH, pkgname, readme, '.git']
    _err_fmt = 'failed to move package file from "%s" to "%s"'
    for source in files:
        if source not in ignore_list:
            _target = os.path.join(pkgname, source)
            _err_msg = _err_fmt % (source, _target)
            with Tools.OnErrorMsg(_err_msg):
                shutil.move(source, _target)

    _err_fmt = 'failed to move residual "%s" to root path'
    with Tools.TemporaryCWD(Config.IGNORE_PATH):
        for source in os.listdir('.'):
            _target = os.path.join('..', source)
            _err_msg = _err_fmt % os.path.join(Config.IGNORE_PATH, source)
            with Tools.OnErrorMsg(_err_msg):
                shutil.move(source, _target)

    _err_fmt = 'failed to delete residual file "%s"'
    _err_msg = _err_fmt % Config.PKGNAME_FNAME
    with Tools.OnErrorMsg(_err_msg):
        os.remove(Config.PKGNAME_FNAME)

    _err_fmt = 'failed to remove dir "%s"'
    _err_msg = _err_fmt % Config.IGNORE_PATH
    with Tools.OnErrorMsg(_err_msg):
        shutil.rmtree(Config.IGNORE_PATH)


def main(argv=sys.argv[1:]):
    flag = all(f(Config.IGNORE_PATH) for f in [os.path.exists, os.path.isdir])
    if flag:
        become_implicit()
    else:
        become_explicit()

    if not argv:
        return

    cmd = ' '.join(argv)
    os.system(cmd)

    if not flag:
        become_implicit()
    else:
        become_explicit()


if __name__ == "__main__":
    main()
