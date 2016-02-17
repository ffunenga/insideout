import os
import shutil
import subprocess

from . import config
from . import tools


def become_explicit():
    with tools.OnErrorMsg('failed to retrieve package name'):
        _cmd = ['python', '-B', 'setup.py', '--name']
        pkgname = subprocess.check_output(_cmd, stderr=subprocess.PIPE)
        pkgname = pkgname.decode('utf-8').strip()

    if not (os.path.exists(pkgname) and os.path.isdir(pkgname)):
        sys.exit('package "%s" folder does not exist' % pkgname)

    _err_msg = 'failed to mkdir "%s"' % config.IGNORE_PATH
    with tools.OnErrorMsg(_err_msg):
        os.mkdir(config.IGNORE_PATH)

    with tools.OnErrorMsg('failed to backup package name'):
        _target = os.path.join(config.IGNORE_PATH, config.PKGNAME_FNAME)
        with open(_target, 'w') as f:
            f.write(pkgname)

    files = list(os.listdir('.'))
    readme = tools.filter_readme(files)
    ignore_list = [config.IGNORE_PATH, pkgname, readme, '.git']
    _err_fmt = 'failed to hide residual entry "%s" in "%s"'
    for source in files:
        if source not in ignore_list:
            _target = os.path.join(config.IGNORE_PATH, source)
            _err_msg = _err_fmt % (source, config.IGNORE_PATH)
            with tools.OnErrorMsg(_err_msg):
                shutil.move(source, _target)

    _err_fmt = 'failed to move package entry "%s" to root path'
    with tools.TemporaryCWD(pkgname):
        for source in os.listdir('.'):
            _target = os.path.join('..', source)
            _err_msg = _err_fmt % os.path.join(pkgname, source)
            with tools.OnErrorMsg(_err_msg):
                shutil.move(source, _target)

    _err_fmt = 'failed to remove package folder "%s"'
    _err_msg = _err_fmt % pkgname
    with tools.OnErrorMsg(_err_msg):
        shutil.rmtree(pkgname)


def become_implicit():
    _fname = os.path.join(config.IGNORE_PATH, config.PKGNAME_FNAME)

    if not (os.path.exists(_fname) and os.path.isfile(_fname)):
        sys.exit('package name file "%s" does not exist' % _fname)

    with tools.OnErrorMsg('failed to retrieve package name'):
        with open(_fname) as f:
            pkgname = f.read().strip()

    with tools.OnErrorMsg('failed to mkdir "%s"' % pkgname):
        os.mkdir(pkgname)

    files = list(os.listdir('.'))
    readme = tools.filter_readme(files)
    ignore_list = [config.IGNORE_PATH, pkgname, readme, '.git']
    _err_fmt = 'failed to move package file from "%s" to "%s"'
    for source in files:
        if source not in ignore_list:
            _target = os.path.join(pkgname, source)
            _err_msg = _err_fmt % (source, _target)
            with tools.OnErrorMsg(_err_msg):
                shutil.move(source, _target)

    _err_fmt = 'failed to move residual "%s" to root path'
    with tools.TemporaryCWD(config.IGNORE_PATH):
        for source in os.listdir('.'):
            _target = os.path.join('..', source)
            _err_msg = _err_fmt % os.path.join(config.IGNORE_PATH, source)
            with tools.OnErrorMsg(_err_msg):
                shutil.move(source, _target)

    _err_fmt = 'failed to delete residual file "%s"'
    _err_msg = _err_fmt % config.PKGNAME_FNAME
    with tools.OnErrorMsg(_err_msg):
        os.remove(config.PKGNAME_FNAME)

    _err_fmt = 'failed to remove dir "%s"'
    _err_msg = _err_fmt % config.IGNORE_PATH
    with tools.OnErrorMsg(_err_msg):
        shutil.rmtree(config.IGNORE_PATH)

