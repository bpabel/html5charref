html5charref
=============

[![Build Status]
(https://travis-ci.org/bpabel/html5charref.svg)]
(https://travis-ci.org/bpabel/html5charref)
[![Docs Status]
(https://readthedocs.org/projects/html5charref/badge/?version=latest)]
(https://readthedocs.org/projects/html5charref/?badge=latest)



Python library for escaping/unescaping HTML5 Named Character References.

The standard library includes the [HTMLParser] library
for unescaping HTML named entities and HTML unicode escapes.  Unfortunately,
it doesn't include any of the named character entity references defined in
[HTML5].  This library intends to provide a solution for escaping/unescaping HTML
character references defined in HTML5.

[HTMLParser]: https://docs.python.org/2/library/htmlparser.html
[HTML5]: http://dev.w3.org/html5/html-author/charref


Installation
------------

This project is still under development, so you should install it via GitHub
instead of PyPI:

```sh
pip install git+https://github.com/bpabel/html5charref.git
```


Usage
-------

The main purpose of html5charref is to unescape HTML.

```python
html = u'This has &copy; and &lt; and &#x000a9; symbols'
print html5charref.unescape(html)
# u'This has \uxa9 and < and \uxa9' 
```

You can also use html5charref to escape individual unicode characters.

```python
import html5charref
# The copyright character
print html5charref.escape_unicode(u'\u00a9')
# u'&copy;'
```


Updating Named Entity References
--------------------------------

It is possible that additional named entity references will be 
added to the HTLM5 spec.  You can update the list maintained by
html5charref by running:

```python
import html5charref
html5charref.update_charrefs()
```


Licensing
---------

This project is licensed under the [MIT] license.

[MIT]: http://opensource.org/licenses/MIT
