#!/usr/bin/env python
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    # GETTING-STARTED: set your app name:
    name='OpenMetroCRM',
    # GETTING-STARTED: set your app version:
    version='0.1',
    # GETTING-STARTED: set your app description:
    description='OpenShift App',
    # GETTING-STARTED: set author name (your name):
    author='Your Name',
    # GETTING-STARTED: set author email (your email):
    author_email='vladistian@gmail.com',
    # GETTING-STARTED: set author url (your url):
    url='http://www.python.org/sigs/distutils-sig/',
    # GETTING-STARTED: define required django version:
    install_requires=requirements,
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
