#!/usr/bin/env python

import os
from setuptools import setup
from marktime import version as module_version


readme_path = os.path.join(os.path.dirname(__file__), 'README.rst')

setup(
    name='marktime',
    version=module_version,
    py_modules=['marktime'],

    description='Python timer module for humans.',
    long_description=open(readme_path).read(),
    license=open('LICENSE').read(),

    author='Eugene Kalinin',
    author_email='e.v.kalinin@gmail.com',

    url='https://github.com/ekalinin/marktime',

    keywords=[
        'timer', 'stopwatch', 'time'
    ],

    platforms='any',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    test_suite='tests'
)
