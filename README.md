# The *insideout* approach to Python packaging

> Why aren't the files inside a Python package the first thing we see when we look at its github repository?

*insideout* is a tool to help you postpone the ugliness of your Python
repository from the viewer's eyes, for example by moving away those ugly
long lists of configuration files that can be seen in almost every open-source
repository.

Take a look at these notorious monstrosities:

* [pypa/pip 8.0.1](https://github.com/pypa/pip/tree/024cfe17e6685483a5a6abfc8983c086267a5a47) ➙ 15 residual files
* [mitsuhiko/flask 0.10](https://github.com/mitsuhiko/flask/tree/3b9574fec988fca790ffe78b64ef30b22dd3386a) ➙ 16 residual files
* [jkbrzt/httpie 0.9.3](https://github.com/jkbrzt/httpie/tree/47220763357f5a25cc535af5c4d2f4f092fb9abd) ➙ 18 residual files

Just look at them: they are **ugly**. Right? There is something unatural to
the way the root directory of those repositories looks like.

## Installation

*insideout* is pure Python code, 2 and 3 compatible. You can download this
repository from github and install it in your environment with:

    $ python __dev__/setup.py install

Or you can also go to PyPI and install from the latest version available their:

    $ pip install insideout

## Background

So, with the single design intention of avoiding as much ugliness as
technically possible in the root directory of your repository, lets look at a
typical example and see what can be improved. Imagine you have the following
source tree:

    $ tree
    .
    ├── package/
    │   ├── __init__.py         # could be in the root directory
    │   ├── main.py             # could be in the root directory
    │   └── tools.py            # could be in the root directory
    ├── tests/              # ugly. should not be here
    │   └── (...)
    ├── tox.ini             # ugly. should not be here
    ├── LICENSE.txt         # ugly. should not be here
    ├── setup.py            # ugly. should not be here
    └── README.md           # ok. Github can generate an HTML page from this.

Basically, what is about to be explained comes down to this:

> A file on the root directory is ugly if it is not absolutely needed when **making use of** the package.

In commerce, prospects are one thing and clients are another. With our
open-source repositories a similar distinction can be made about the python
developers who look at them: the ones who use our code are one thing and the
ones who further contribute to it are another. Hence, the adjective *ugly*
herein used, is analyzed from the first perspective only: the developer who
**at most** makes use your code, without any intentions of further
developing, testing or deploying it.

This tightens the interpretation of the adjective *ugly* to a point where
there isn't much margin for subjective though. For example, from this
perspective it is obvious that `license.txt` should be absolutely postponed
from the viewer's eyes, simply because it is not needed to make use of the
code in the package. The same applies to the `tests` directory. If you want
to focus the use of tests in your project, write about it on the `README`
file, for example. These types of entries on your repository root's are ugly
and their observation should be postponed to a later moment.

With `insideout` we can pull the package source files to the root directory,
and push all the residual testing/configuration files and folders away from
sight. A folder called `__dev__` is created for this purpose:

    $ insideout
    $ tree
    .
    ├── __dev__/
    │   ├── tests/              # ok. no longer ugly
    │   ├── setup.py            # ok. no longer ugly
    │   ├── tox.ini             # ok. no longer ugly
    │   └── (...)               # remaining ugly files/folders went all here
    ├── README.md             # ok. Github can generate an HTML page from this.
    ├── __init__.py           # ok. explicitly observable, nice!
    ├── main.py               # ok. explicitly observable, nice!
    └── tools.py              # ok. explicitly observable, nice!

Its almost the same as turning a t-shirt inside out. For example, the
`README.md` was left behind in order to allow presenting an HTML page on
github. There is also some caution in place to avoid moving the `.git`
folder. This resulting structure is reversible to the previous structure by
re-executing the command `insideout`.

## Workflow

The problem now, is that `setup.py` is not on a folder level immediatly
above to the package level, which makes it complicated to generate
distributions or install the package. This is solved in at least the
following two ways.

#### `setup.py` fix

It is actually easy to solve the directory problem by the adding the
following code to the begging of your `setup.py` file:

```python
import os
import shutil

PACKAGE_NAME = '<...package name goes here>'

_t = os.path.abspath(__file__)
cwd = os.path.dirname(_t)
if os.path.basename(cwd) == '__dev__':
    os.chdir(cwd)
    shutil.rmtree(PACKAGE_NAME, ignore_errors=True)
    ignore_list = shutil.ignore_patterns('__dev__*', '.git*', 'env*', '.tox')
    shutil.copytree('..', PACKAGE_NAME, ignore=ignore_list)
```

And that's it. That code enables the `setup.py` to work as expected from
anywhere.

From the root of the repository you can run these:

    $ python __dev__/setup.py install
    $ tox -c __dev__/tox.ini

From inside __dev__ you can run these:

    $ python setup.py install
    $ tox

Even if you reorganize your code in the classical testing/deployment focused
structure (where all the test configuration files, license, etc., are placed
in the root directory of your repository) then this setup.py still works.

#### (alternative) prefix `git` commands with `insideout`

If you don't want to touch in your `setup.py`, then, in order to maintain
your public version (the one accesible throught github) in the explicit
form, you can work locally on your project with the *ugly* files on the root
directory by preforming the following steps:

1. Clone the intended git repository: `$ git clone <clone_url>`
2. Swap files to the insideout style: `$ insideout`
3. Prefix all `git` commands with *insideout*. Examples:
    - `$ insideout git status`
    - `$ insideout git add compiler.py`
    - `$ insideout git commit -m "adds compiler"`
    - `$ insideout git push origin master`
