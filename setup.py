#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages            #这个包没有的可以pip一下

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = "luadata",
    version = "0.0.3",
    keywords = ("pip", "lua", "data"),
    description = "Serialized Python list & dictionary to Lua table.",
    long_description = long_description,
    long_description_content_type="text/markdown",
    license = "BSD License",

    url = "https://github.com/leafvmaple/luadata",
    author = "Leafvmaple",
    author_email = "leafvmaple@gmail.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    #install_requires = ["codecs"]
)