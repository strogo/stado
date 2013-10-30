*stadø*
=======



**What is stado?**

Stado is minimalistic static site generator powered by python scripts.
You just download `stado.py` and it is ready to work.



[![Build Status](https://travis-ci.org/lecnim/stado.png?branch=master)](https://travis-ci.org/dendek/stado)


**What? Why another static site generator?**

Stado is different:

- No dependencies, batteries are included: 
  - markdown support using great [`Python-Markdown`](https://github.com/waylan/Python-Markdown)
  - mustache templates using great [`pystache`](https://github.com/defunkt/pystache)
  - yaml parsing using great [`pyyaml`](https://github.com/yaml/pyyaml)
- Only one file (actually less than **100kb**).
- Pages creation powered by python scripts.
- Site content from **yaml** or **json** files.
- Development server.
- File watcher for site auto-rebuilding.
- Manage group of sites *(can build or watch more than one site)*.
- **Easy** and minimalistic.

Stado is best for small, files driven sites. You can use python scripts so the sky
is the limit, probably.


**What do I need?**

> Only python3, currently supported versions: `3.2`, `3.3`


**Is it ready?**

Very, very close to first production release. Only code cleaning and some testing left.

![gg](logo.jpg)

Quick guide
===========

Install
-------

Just download `stado.py` file to empty directory.



Example
-------

Stado uses `stado.py` - python script file to build site. Pages are rendered using
template engine, it is Mustache by default.

**Example directory structure:**

```
stado.py
project/
    site.py             # python script which builds site
    index.html          # page
    image.jpg           # asset
```

*File `project/site.py`:*
```python
from stado import run
run()                   # start building site.
```
*This python script is controlling site rendering. Use `run()` method to start it.
Controllers objects like `@before` are available to control rendering process.*


**Run stado:**
```
stado.py build project
```

*Stado renders site to `output` directory:*
```
project/
    site.py
    index.html
    image.jpg
    output/             # rendered site is here
        index.html
        image.jpg
```

By default all `html`, `md`, `json`, `yaml` files are rendered using template engine
and saves as a `html` pages. These are called **pages**.
Other files like `image.jpg` are just copied. These are called **assets**.


Commands
--------

#### help ####


Shows help about commands.

`help build`

Shows general help.

`help`



#### edit ####

Auto rebuild on save, and start development server.

`edit project`

Use custom output directory.

`edit project --output /www/project`



#### build ####

Build site.

`build project`

Build all sites in stado directory.

`build`

Use custom output directory.

`build project --output /www/project`



#### watch ####

Rebuild site on save.

`watch project`

Watch all sites in stado directory and rebuild on save.

`watch`

Use custom output directory.

`watch --output /www`





Controllers
===========


`@before`
---------

Use `@before` decorator to execute function before page rendering. It is used
to add variables to page context.

#### Example: ####

```python
from stado import run, before

@before('index.html')
def add_title():
    return {'title': 'Hello'}

run()
```

*File `index.html`:*
```jinja
{{ title }}
```

*Rendered file `output/index.html`:*
```HTML
Hello
```

#### Details: ####

- `@before` can take any number of paths and also supports file matching.
  ```python
  @before('index.html', '*.html')
  def add_title():
      return {'title': 'Hello'}
  ```


- `@before` can pass page object to function using function first argument.
  ```python
  @before('index.html')
  def add_title(page):
      page['title'] = page.source
  ```


`@after`
--------

Use `@after` decorator to execute function **after** pages rendering. It is used to
modify page content before writing it in output.

#### Example ####

```python
from stado import run, after

@after('index.html')
def capitalize(content):
    return content.capitalize()

run()
```

*File `index.html`:*
```
hello world
```

*Rendered file `output/index.html`:*
```
HELLO WORLD
```

#### Details ####

- `@after` as like `@before` can take any number of paths and also supports file matching.

- `@after` can pass page object to function using it **second** argument.
```python
@after('*.html')
def censure(content, page):
    if page.filename == 'index.html'
        return 'censored'
```



`layout`
--------

Use `layout` to render page content using layouts files.

#### Example ####

```python
from stado import run, layout
layout('index.html', 'layout.html')
run()
```

*File `index.html`:*
```HTML
<p>Hello badger!</p>
```

*File `layout.html`:*
```jinja
<h1>Layout</h1>
{{{ content }}}
```

*Rendered file `output/index.html`:*
```HTML
<h1>Layout</h1>
<p>Hello badger!</p>
```

#### Details ####

- `layout` can be used inside function decorated by `@before`.
  ```python
  @before('index.html')
  def set_layout(page):
      layout(page, 'layout.html')
  ```

- `layout` can render page using multiple layout files.
  ```python
  layout('index.html', 'sub-layout.html', 'layout.html')
  ```
  
  *File `index.html`:*
  ```
  Hello badger!
  ```
  
  *File `sub-layout.html`:*
  ```jinja
  Hello sub-layout!
  {{{ content }}}
  ```
  
  *File `layout.html`:*
  ```jinja
  Hello layout!
  {{{ content }}}
  ```
  
  *Rendered file `output/index.html`:*
  ```
  Hello layout!
  Hello sub-layout!
  Hello badger!
  ```


- `layout` has access to page context using `{{ page }}` variable.
  ```jinja
  {{ page.title }}
  {{{ content }}}
  {{ page.footer }}
  ```

- You can pass custom context to layout using `context` argument.
  ```python
  layout('index.html', 'layout.html', context={'title': 'Badger'})
  ```
  
  Then you can use this context in `layout.html`:
  ```jinja
  {{ title }}
  ```


`permalink`
-----------

Use `permalink` to change page or asset url.

#### Example ####

```python
permalink('index.html', '/welcome.html')
```

*Page `index.html` will be written in output as a `welcome.html`.*

#### Details ####

- Permalink supports keyword variables like:
  - `:path`, relative path to content, example: `images/face.jpg`
  - `:filename`, content filename, example: `face.jpg`
  - `:name`, name of file without extension, example: `name`
  - `:extension`, file extension, example: `jpg`

  *Use of permalink keyword variables:*
  ```python
  permalink('index.html', '/:path/:name/index.html')
  ```

- You can use predefined permalink styles like:
  - `pretty => /:path/:name/index.html`
  - `default => /:path/:filename`


`ignore`
--------

Use `ignore` to ignore certain paths. For example ignore file names with an underscore
at the beginning:
```python
ignore('_*')
```

`@helper`
---------

Use `@helper` decorator to have access to function during template rendering.

#### Example ####

```python
@helper
def hello():
    return 'Hello badger!'
```

Template:
```jinja
{{ hello }}
```

Rendered template:
```
Hello badger!
```

#### Details ####

- Helper function can return `list`, `dict` or other objects:
  ```python
  @helper
  def numbers():
      return [1, 2, 3, 4]
  ```
  
  *Template:*
  ```jinja
  {{# numbers }}{{.}}{{/ numbers }}
  ```
  
  *Rendered template:*
  ```
  1234
  ```


- Function decorated by `@helper` can use `pages` and `assets`. This controllers returns list
  of Pages object or Assets objects. For example:
  
  Example project structure:
  
  ```
      project/
          site.py
          index.html
          welcome.html
          contact.html
  ```
  
  *File `site.py`:*
  ```python
  from stado import helper, run
  
  @helper
  def menu():
      return [i for i in pages('*.html')]
  
  run()
  ```
  
  *File `index.html`:*
  ```jinja
  {{# menu }}
  <a href='{{ url }}'>Page</a>
  {{/ menu }}
  
  ```
  
  *Rendered file `output/index.html`:*
  ```HTML
  <a href='index.html'>Page</a>
  <a href='welcome.html'>Page</a>
  <a href='contact.html'>Page</a>
  ```




Page class or Asset class
-------------------------

This class represent page. Properties:
```
source
    Relative path to source file, example: 'page.html'
filename
    Source filename.
template
    Un-rendered page content.
url
    Page will be available in this URL.
context
    Dictionary passed to template during rendering.
output
    Output path, relative.
```

You can access page context using dict brackets:
```python
page[title] == page.context['title']
```




To be done:
```

- [ ] Quick-guide
- [ ] Basic documentation

```


**Where are docs?**

Only quick guide!
