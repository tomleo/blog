# Todos

- [ ] Integrate pytest & converage
- [ ] Render more meta data to the template
- [ ] Add basic styling to pages
- [ ] Add breadcrumb navigation (generate based on path)
- [x] Add clean command for the build folder
- [ ] Skip rendering HTML for markdown files without content
- [ ] Private doc integration
- [ ] Roll up pages
- [ ] Generate `<name>.html` `<name>-body.json`
- [ ] If no metadata for title, extract h1 (i.e. `#`) from file and use that
- [ ] If no metadata for lastmod, get last modified from physical file

## Highlevel Goals

**Setting up a static website generator process**:

```console
$ mkdir my-blog
$ mkdir my-blog/content
$ cd my-blog/content
$ python -m venv venv
$ source venv/bin/activate
$ pip install blog
$ blog build content
Reading blog_config.yaml
    - config file missing
    - creating config file
    - blog_config.yaml created, output:
          source_directory: "./content/"
          build_directory: "./build/"
          theme: "default"
          rsync: null
Building html
    - build directory missing
    - creating build directory
Finding files for build
Found: 0 files
Success: 0 files created, 0 files updated, 0 files deleted
$ blog build content
Reading blog_config.yaml
Building html
Finding files for build
Found: 0 files
Success: 0 files created, 0 files updated, 0 files deleted
```

Given a file `content/hello.md`
Create `build/hello.html`, contains a static HTML page
Create `build/hello.html.partial`, contains a static HTML page of only the "body" for use with pjax
Create `build/hello.json`, last modified time, author, categories, title, checksum, permissions, publish date, ect.

**Serving Content**:

`blog-server.py` does the following:
- Reads through build directory
- Generates JSON data looking like:

```
{
    "hello.html": {
        "html" "/home/nginx/build/hello.html",
        "partial": "/home/nginx/build/hello.html.partial",
        "meta": {
            "lastmod": "<utc timestamp>",
            "author": "<author>",
            "categories": [],
            "title": "<title>",
            "checksum": "<checksum of html file>",
            "permissions": "private",
            "pubdate": "<utc timestamp>"
        }
    }
}
```
- Caches JSON data in memory

Request Logic
```
1. HTTP GET /hello.html
2. Read entry 
2a. if private, check credentials (async call to firebase)
2b. if pubdate > now, 404
3. Return 200 response with content of file (also sets e-tag and/or other cache control headers)

Once on the page JS kicks in:
1. HTTP (Ajax) GET /hello.html
2. Show ajax spinner, set timeout
3. Return hello.html.partial which is inserted into the page
```

**Editing Content:**

- Relational Database & Django backend
    - Basic login and permissions
    - Database keeps (in a normalized way) authors, tags, ect.
- Front-end is JS SPA, with an markdown editing interface easy to use by non-devs
- A public command:
    1. will write to a directory `blog` knowns about
    2. `blog` will generate HTML from `md` files
    3. rsync command to get them onto `blog-server.py` server


## Private doc integration

Integrate with django private docs project?
- Private docs configured by metadata?
- Recipients: ["tomjleo@gmail.com"] + one-time password via email

## Roll up pages

### Generate trello category page

List each category with links to the HTML files

### Reading metrics

List what was read in order by timestamp (include markdown files without content)

## Generate `<name>.html` `<name>.json`

*foo.md*
```markdown
# Test

This is a test
```

*foo.html*
```html
<html>
<head><!-- ... --></head>
<body>
    <h1>Test</h1>
    <p>This is a test</p>
</body>
</html>
```

*foo.json*
```json
{
    'head-append': [
        '<link rel="stylesheet" type="text/css" href="link-to-page-style.css" />'
    ],
    'body': '<h1>Test</h1><p>This is a test</p>'
}
```
