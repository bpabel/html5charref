"""
Python library for escaping/unescaping HTML5 Named Character References.


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


def escape_unicode(c):
    """
    Return an HTML5 named character reference for the given
    unicode character.  If no character entity reference is available,
    return a an html unicode escape, or the original unicode char if 
    that cannot be done.
    
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
    else:
        # Use a unicode point escape if no named entity exists.
        try:
            return '&#x{0:05x};'.format(ord(c))
        except TypeError:
            # Catches surrogate pair errors for high unicode code points.
            return c


def escape_unicode_advanced(c):
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


