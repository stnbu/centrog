# -*- coding: utf-8 -*-

_author = 'Mike Burr'
_email = 'mburr@unintuitive.org'
__author__ = '%s <%s>' % (_author, _email)

from distutils.core import setup
import time

# my modules
import centrog

# README.rst dynamically generated:
with open('README.md', 'w') as f:
    f.write(centrog.__doc__)

NAME = centrog.__name__

def read(file):
    with open(file, 'r') as f:
        return f.read().strip()

setup(
    name=NAME,
    version='0.0.1-%s' % int(time.time()),  # development hack
    description='Fast, simple syslog database explorer',
    long_description=read('README.md'),
    author=_author,
    author_email=_email,
    provides=[NAME],
    requires=['flask', 'flask_wtf', 'psycopg2'],
    packages=[NAME],
    package_data={'centrog': ['templates/*']},
    scripts=[
        'bin/centrog-www-server-test-server',
    ],
)