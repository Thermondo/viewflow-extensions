#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import codecs
import os

from setuptools import find_packages, setup


def read(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    return codecs.open(file_path, encoding='utf-8').read()


PACKAGE = "viewflow_extensions"
NAME = "viewflow-extensions"
DESCRIPTION = "Useful extensions for django-viewflow."
AUTHOR = "Johannes Hoppe, Thermondo GmbH"
AUTHOR_EMAIL = "johannes.hoppe@thermondo.de"
URL = "https://github.com/Thermondo/viewflow-extensions"
VERSION = __import__(PACKAGE).__version__


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    download_url=URL,
    packages=find_packages(exclude=[
        "*.tests", "*.tests.*", "tests.*", "tests", ".egg-info"
    ]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
    ],
    install_requires=[],
    zip_safe=False,
)
