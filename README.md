# The *insideout* approach to Python packaging

> Why aren't the files inside a Python package the first thing we see when we look at its github repository?

*insideout* is a tool to help you postpone the ugliness of your python
repository from the viewer's eyes, for example by moving away those ugly
long lists of configuration files or legal files (e.g. `license.txt`,
`authors.txt`) that can be seen in almost every open-source repository.

Take a look at these exemplary monstrosities:

* [pypa/pip 8.0.1](https://github.com/pypa/pip/tree/024cfe17e6685483a5a6abfc8983c086267a5a47) ➙ 15 residual files
* [mitsuhiko/flask 0.10](https://github.com/mitsuhiko/flask/tree/3b9574fec988fca790ffe78b64ef30b22dd3386a) ➙ 16 residual files
* [jkbrzt/httpie 0.9.3](https://github.com/jkbrzt/httpie/tree/47220763357f5a25cc535af5c4d2f4f092fb9abd) ➙ 18 residual files

Just look at them: they are **ugly**. Right? There is something unatural to
the way the root directory of those repositories looks like.

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

Basically, what is about to be explained about this structure comes down to
this:

> The files on the root directory of your repository are ugly if they are not absolutely needed to **make use of** your package.

In commerce, prospects are one thing and clients are another. With our
open-source repositories a similar distinction can be made about the python
developers who look at them: the ones who use our code are one thing and the
ones who actually develop and contribute to it are another.

The adjective *ugly* herein used, is analyzed from the developer who **at most**
makes use your code (without any intentions of developing, testing or deploying
it). This tightens the interpretation of the adjective *ugly* to a point
where there isn't much margin for subjective, empirical though. For example, from this
perspective it is obvious that `license.txt` should be absolutely postponed
from the viewer's eyes, simply because it is not needed to make use of the code
in the package. The same applies to the `tests` directory. If you want to
focus the use of tests in your project, write about it on the `README`
file, for example.

With `insideout` we can pull the package source files to the root
directory, and push all the residual development files and folders away from
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

Its almost the same as turning a t-shirt inside out. The small difference is
that the files and folders are not completely turned *inside out*.
For example, the `README.md` was left behind in order to allow presenting an
HTML page on github. There is also some caution in place to avoid moving the
`.git` folder.

reverse the previous swap using the same command: `insideout`.

*insideout* is pure Python code, 2 and 3 compatible.

## Workflow

With *insideout* the objective is to keep your public version in the
explicit form.  The problem is that you need to work on your project in the
implicit from (i.e. with the *ugly* files on the root directory).

The `insideout` command allows the following workflow:

1. Clone the intended git repository: `$ git clone <clone_url>`
2. Swap files to the implicit form: `$ insideout`
3. Prefix all git commands with *insideout*. Examples:
    - `$ insideout git status`
    - `$ insideout git add compiler.py`
    - `$ insideout git commit -m "adds compiler"`
    - `$ insideout git push origin master`
