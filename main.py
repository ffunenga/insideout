import sys
import os

from . import config
from . import actions


def main(argv=sys.argv[1:]):
    flag = all(f(config.IGNORE_PATH) for f in [os.path.exists, os.path.isdir])
    if flag:
        actions.become_implicit()
    else:
        actions.become_explicit()

    if not argv:
        return

    cmd = ' '.join(argv)
    os.system(cmd)

    if not flag:
        actions.become_implicit()
    else:
        actions.become_explicit()
