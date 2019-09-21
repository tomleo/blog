# Todos

- [ ] Add basic styling to pages
- [ ] Add breadcrumb navigation (generate based on path)
- [ ] Render more meta data to the template
- [ ] Skip rendering HTML for markdown files without content
- [x] Add clean command for the build folder
- [ ] Private doc integration
- [ ] Roll up pages
- [ ] Generate `<name>.html` `<name>-body.json`

## Naming Project

SatGen
YASG
Static Simple
Markdown Pub


## Private doc integration

Integrate with django private docs project?
- Private docs configured by metadata?
- Recipients: ["tomjleo@gmail.com"] + one-time password via email

# Roll up pages

## Generate trello category page

List each category with links to the HTML files

## Reading metrics

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