# insideout

> Why aren't the files inside a Python package the first thing we see when we look at its github repository?

*insideout* is a tool to swap the files on your repository's root directory
with the ones inside your python package, and vice-versa. This tool makes the
term "repository" **literally** equivalent to the term "Python package".

It works like this:

    $ tree
    .
    ├── tests               # this is a typical directory with tests
    │   └── (...)
    ├── package             # this package is an example
    │   ├── __init__.py
    │   ├── main.py
    │   └── tools.py
    ├── LICENSE.txt         # residual file
    ├── README.md           # residual file
    ├── setup.py            # residual file
    └── tox.ini             # residual file

    2 directories, 9 files
    $ insideout
    $ tree
    .
    ├── tests               # untouched folder
    │   └── (...)
    ├── metafiles           # residual files went inside this folder
    │   ├── LICENSE.txt       # residual file
    │   ├── setup.py          # residual file
    │   └── tox.ini           # residual file
    ├── README.md           # residual file left behind on purpose
    ├── __init__.py         # source-code file
    ├── main.py             # source-code file
    └── tools.py            # source-code file

    2 directories, 9 files

```python setup.py --name``` was used to automaticly inspect the name of
the package and imediatly swap the files inside its respective folder.

You can reverse the previous swap using the same command: ```insideout```.

*insideout* is pure Python code, 2 and 3 compatible.

## Bad examples

Take a look at these huge root directories:

* [pypa/pip 8.0.1](https://github.com/pypa/pip/tree/024cfe17e6685483a5a6abfc8983c086267a5a47) ➙ 15 residual files
* [mitsuhiko/flask 0.10](https://github.com/mitsuhiko/flask/tree/3b9574fec988fca790ffe78b64ef30b22dd3386a) ➙ 16 residual files
* [jkbrzt/httpie 0.9.3](https://github.com/jkbrzt/httpie/tree/47220763357f5a25cc535af5c4d2f4f092fb9abd) ➙ 18 residual files
