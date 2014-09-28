"""
html5charref
=============

Python library for escaping/unescaping HTML5 Named Character References.

The standard python library includes the `HTMLParser`_ package
for unescaping HTML named entities and HTML unicode escapes.  Unfortunately,
it doesn't include any of the named character entity references defined in
`HTML5`_.  This library intends to provide a solution for 
escaping/unescaping HTML character references defined in HTML5.

.. _HTMLParser: https://docs.python.org/2/library/htmlparser.html
.. _HTML5: http://dev.w3.org/html5/html-author/charref


Installation
------------

This project is still under development, so you should install it via GitHub
instead of PyPI::

    pip install git+https://github.com/bpabel/html5charref.git



Usage
-------

The main purpose of html5charref is to unescape HTML named entities.  It 
will also handle HTML unicode character escapes.

::

    html = u'This has &copy; and &lt; and &#x000a9; symbols'
    print html5charref.unescape(html)
    # u'This has \uxa9 and < and \uxa9 symbols' 


You can also use html5charref to find the HTML5 named entity for a given
unicode character.

::

    import html5charref
    # The copyright character
    print html5charref.escape_char(u'\u00a9')
    # u'&copy;'



Updating Named Entity References
--------------------------------

It is possible that additional named entity references will be 
added to the HTLM5 spec.  You can update the list maintained by
html5charref using the :func:`update_charrefs` function.  This queries
the latest named entity definitions from the w3 HTML5 site.

::

    import html5charref
    html5charref.update_charrefs()



Licensing
---------

This project is licensed under the `MIT`_ license.

.. _MIT: http://opensource.org/licenses/MIT



API Reference
--------------

"""


import os
import re
import json


__version__ = '0.1.0'

UPDATE_URL = r'http://dev.w3.org/html5/html-author/charref'
CACHE_FILENAME = 'data/html5charref.json'

charref_map = None
unicode_map = None


def update_charrefs():
    """
    Update the named entity dictionary from the w3 html5 specification site.    
    
    """

    import requests
    import BeautifulSoup as bs

    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), CACHE_FILENAME)
    r = requests.get(UPDATE_URL)
    soup = bs.BeautifulSoup(r.text)
    escape_map = dict()
    for row in soup.table.contents:
        if isinstance(row, bs.Tag):
            escape_codes = row.contents[1].text.replace('&amp;', '&').split(' ')

            match = re.match(r'&#x([a-f0-9]{5});', row.contents[0].text, flags=re.I)
            if match:
                unicode_char = '\\U000{0}'.format(match.group(1)).decode('unicode-escape')
                for escape_code in escape_codes:
                    escape_map[escape_code] = unicode_char

    with open(filepath, 'w') as f:
        json.dump(escape_map, f, sort_keys=True, separators=(',', ': '), indent=0)


def _load_charrefs():
    """
    Loads the cached character entity reference information from disk.
    
    """
    global charref_map
    global unicode_map

    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), CACHE_FILENAME)
    if not os.path.isfile(filepath):
        update_charrefs()

    with open(filepath, 'r') as f:
        charref_map = json.load(f)

    # Store the reverse lookup as well.
    # Some named character references refer to the same unicode point
    # (e.g. &lsqb; &lbrack), so the matching escape codes are stored as
    # a list.
    unicode_map = dict()
    for escape_code, unicode_char in charref_map.iteritems():
        unicode_map.setdefault(unicode_char, []).append(escape_code)


def unescape_charref(charref):
    """
    Return the matching unicode character for the given HTML5
    named character reference.    
    
    """
    if charref_map is None:
        _load_charrefs()

    return charref_map.get(charref, charref)


def escape_char(c, named_only=False):
    """
    Return an HTML5 named character reference for the given
    unicode character.  If no character entity reference is available,
    return a an html unicode escape, or the original unicode char if 
    that cannot be done.  Characters that are part of ASCII are not escaped.
    
    :param bool named_only:  If set to True, will only try to use
        named entities.  If a named entity can't be found, the original
        character will be returned instead of an html unicode escape.
    
    .. note::
    
        Because several character references may refer to the same
        unicode point, the returned character reference may not be
        the one you expect.  Use the :func:`escape_unicode_advanced` 
        function to get a list of all named character references 
        for a given unicode point and choose the specific one you want.
    
    """
    if unicode_map is None:
        _load_charrefs()

    charrefs = unicode_map.get(c)
    if charrefs:
        if len(charrefs) > 1:
            # If more than one named entity exists, choose the
            # all-lowercase version if it exists.
            for charref in charrefs:
                if re.match('&[a-z]+;', charref):
                    return charref
        return charrefs[0]

    elif named_only:
        return c

    else:
        # Don't try to unicode escape ascii chars.
        try:
            if ord(c) < 128:
                return c
        except TypeError:
            return c

        # Use a unicode point escape if no named entity exists.
        try:
            return '&#x{0:05x};'.format(ord(c))
        except TypeError:
            # Catches surrogate pair errors for high unicode code points.
            return c



def escape_char_advanced(c):
    """
    Return a list of all HTML5 named character references for the given
    unicode character.    
    
    """
    if unicode_map is None:
        _load_charrefs()

    return unicode_map.get(c)


def unescape(html):
    """
    Return a unicode string with html character entity references and 
    html unicode escapes converted to their unicode equivalent.
    
    This closely matches HTMLParser.unescape(), but supports the
    HTML5 named entities.
    
    """

    if '&' not in html:
        return html

    def repl(m):
        s = m.group(1)
        try:
            if s[0] == "#":
                s = s[1:]
                if s[0] in ['x', 'X']:
                    c = int(s[1:], 16)
                else:
                    c = int(s)
                return unichr(c)
        except ValueError:
            return '&#' + s + ';'
        else:
            s = '&' + s + ';'
            return unescape_charref(s)

    return re.sub(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));", repl, html)


