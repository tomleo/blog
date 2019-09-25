# Blog

This is a simple static site generator. It traverses through a source directory of markdown files and creates a
destination directory with equivalent HTML files.

```
Markdown In -> HTML Out
```

## Installation

```
$ python3.7 -m venv venv
$ source venv/bin/activate
$ pip install blog
```

## Usage

```
(venv) $ python -m blog build /path/to/source-dir /path/to/build-dir
```

## Simple by design

- Nothing smart is done around friendly URLs / generating folders with `index.html` files
    + If you want an `index.html` file, create an `index.md` file in your source directory
- There is no database
- There is no configuration (for now)

**Need something more complex?**

- Consider using Hugo, Gatsby, Django, writing your own server
