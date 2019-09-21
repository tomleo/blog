# Simple Blog

- Markdown files in `content/` directory are converted to HTML
- Directory structure and files are mirrored in `build/` folder

## Usage

Building the docs is done via the following:
```
./main.py build
```

To see the results locally do the following:
```
./main.py serve
```

## Simple by design

- Nothing smart is done around generating `index.html` files for use with HTTP servers / friendly URLs
- There is no database

**Need something more complex?**

- Consider using Hugo, Gatsby, Django, writing your own server

Package Structure based on:
https://github.com/pypa/sampleproject
