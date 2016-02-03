# insideout

> Why aren't the files inside a Python package the first thing we see when we look at its github repository?

*insideout* is a tool to swap the files on your repository's root directory
with the ones inside your python package, and also reverse that operation.

Imagine you have the following source tree:

    $ tree
    .
    ├── package
    │   ├── __init__.py     # should be in the root directory
    │   ├── main.py         # should be in the root directory
    │   └── tools.py        # should be in the root directory
    ├── README.md           # ok. Github can generate an HTML page from this.
    ├── LICENSE.txt         # ugly. should not be here
    ├── setup.py            # ugly. should not be here
    └── tox.ini             # ugly. should not be here

    1 directory, 7 files

Now, with the `insideout` tool we
will pull the package files to the root directory, and push
all the residual development files (marked as *ugly* above) away from sight.

    $ insideout
    $ tree
    .
    ├── metafiles
    │   ├── package_name.txt  # backup file with the package name
    │   └── (...)               # ugly files went here
    ├── README.md             # ok. Github can generate an HTML page from this.
    ├── __init__.py           # ok. explicitly observable
    ├── main.py               # ok. explicitly observable
    └── tools.py              # ok. explicitly observable

    1 directory, 8 files

`README.md` was left behind in order to
allow presenting an HTML page on github. `metafiles/__pkgname.txt` file
was created to backup the package name, which now allows to reverse the
previous swap using the same command: `insideout`.

*insideout* is pure Python code, 2 and 3 compatible.

## Workflow

With *insideout* the objective is to keep your public version in the
explicit form.  The problem is that you need to work on your project in the
implicit from (i.e. with the *ugly* files on the root directory).

The `insideout` command allows the following workflow:

1. Clone the intended git repository: `git clone <clone_url>`
2. Swap files to the implicit form: `insideout`
3. Prefix all git commands with *insideout*. Examples:
    - `insideout git status`
    - `insideout git add compiler.py`
    - `insideout git commit -m "adds compiler"`
    - `insideout git push origin master`

## Bad examples

Take a look at these huge root directories:

* [pypa/pip 8.0.1](https://github.com/pypa/pip/tree/024cfe17e6685483a5a6abfc8983c086267a5a47) ➙ 15 residual files
* [mitsuhiko/flask 0.10](https://github.com/mitsuhiko/flask/tree/3b9574fec988fca790ffe78b64ef30b22dd3386a) ➙ 16 residual files
* [jkbrzt/httpie 0.9.3](https://github.com/jkbrzt/httpie/tree/47220763357f5a25cc535af5c4d2f4f092fb9abd) ➙ 18 residual files
