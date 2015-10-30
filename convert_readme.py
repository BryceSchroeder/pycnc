#!/usr/bin/python
# coding: utf-8

r"""
"""

import pypandoc

# converts markdown to reStructured
z = pypandoc.convert('README.md', 'rst', format='md')

# writes converted file
with open('README.rst', 'w') as outfile:
    outfile.write(z)
