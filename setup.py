from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import html5charref

here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = 'Python library for escaping/unescaping HTML5 Named Character References'

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='html5charref',
    version=html5charref.__version__,
    url='http://github.com/bpabel/html5charref/',
    license='MIT',
    author='Brendan Abel',
    tests_require=['pytest'],
    install_requires=[
        'requests>=2.2.0',
        'BeautifulSoup>=3.2.1',
    ],
    cmdclass={'test': PyTest},
    author_email='007brendan@gmail.com',
    description=long_description,
    long_description=long_description,
    packages=['html5charref'],
    include_package_data=True,
    platforms='any',
    test_suite='html5charref.tests.test_html5charref',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Text Processing :: Markup',
        'Topic :: Text Processing :: Markup :: HTML',
        ],
    extras_require={
        'testing': ['pytest'],
    }
)
