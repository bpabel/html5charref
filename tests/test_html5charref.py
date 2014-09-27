
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import html5charref


def test_escape_unicode():
    s = u'a'
    es = u'&#x00061;'
    assert html5charref.escape_unicode(s) == es

    s = u'\u00a9'
    es = u'&copy;'
    assert html5charref.escape_unicode(s) == es

    s = u'<'
    es = u'&lt;'
    assert html5charref.escape_unicode(s) == es

    s = u'\u0229'
    es = u'&#x00229;'
    assert html5charref.escape_unicode(s) == es


def test_escape_unicode_advanced():
    s = u'\u00a9'
    es = ['&COPY;', '&copy;']
    assert html5charref.escape_unicode_advanced(s) == es

    s = u'a'
    es = None
    assert html5charref.escape_unicode_advanced(s) == es


def test_unescape():
    s = u'a'
    es = u'a'
    assert html5charref.unescape(es) == s

    s = u'a'
    es = u'&#x00061;'
    assert html5charref.unescape(es) == s

    s = u'\u00a9'
    es = u'&copy;'
    assert html5charref.unescape(es) == s

    s = u'<'
    es = u'&lt;'
    assert html5charref.unescape(es) == s

    s = u'\u0229'
    es = u'&#x00229;'
    assert html5charref.unescape(es) == s


def test_update_charrefs():
    filepath = os.path.join(
        os.path.dirname(os.path.abspath(html5charref.__file__)),
        html5charref.CACHE_FILENAME,
    )
    mtime = None
    if os.path.isfile(filepath):
        mtime = os.path.getmtime(filepath)

    html5charref.update_charrefs()

    assert os.path.isfile(filepath)
    assert os.path.getmtime(filepath) != mtime

