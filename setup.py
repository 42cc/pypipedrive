#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join, dirname
from setuptools import setup, find_packages

setup(
    name='pypipedrive',
    version='0.1.1',
    packages=find_packages(),
    requires=['python (>= 2.7)', 'requests'],
    install_requires=['requests'],
    description='Python wrapper for the Pipedrive API',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='Andriy Sheerpa',
    author_email='asherepa@gmail.com',
    url='https://github.com/42cc/pypipedrive',
    download_url='https://github.com/42cc/pypipedrive/tarball/master',
    license='BSD License',
    keywords=['pipedrive', 'api'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
)
