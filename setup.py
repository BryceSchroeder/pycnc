# coding: utf-8

import io

from setuptools import setup
import pypandoc

import pycnc

files = []


# setup(name="pycnc", version="1.0", description="Generates EMC2 GCode for simple 2.5D shapes",
#       author="Guillaume Florent", author_email="florentsailing@gmail.com", url="None yet",
#       packages=['pycnc', 'pycnc.examples', 'pycnc.tests'],
#       # package_data = {'pycnc' : files },
#       scripts=[], long_description="""Generates EMC2 GCode for simple 2.5D shapes""")

setup(
    name='pycnc',
    version=pycnc.__version__,
    url='http://github.com/floatingpointstack/pycnc/',
    license='GPL v2',
    author='Guillaume Florent',
    test_suite='nose.collector',
    install_requires=[],
    author_email='florentsailing@gmail.com',
    description='2.5D CNC Python routines to generate GCode for simple geometries',
    long_description=pypandoc.convert('README.md', 'rst'),
    packages=['pycnc'],
    include_package_data=True,
    platforms='any',
    test_suite='pycnc.tests.test_pycnc',
    # classifiers list at : https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        ],
)
