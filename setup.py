# coding: utf-8

import io
import os

from setuptools import setup, find_packages

import pycnc

files = []

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read(os.path.join(os.path.dirname(__file__), './README.rst'))

# setup(name="pycnc", version="1.0", description="Generates EMC2 GCode for simple 2.5D shapes",
#       author="Guillaume Florent", author_email="florentsailing@gmail.com", url="None yet",
#       packages=['pycnc', 'pycnc.examples', 'pycnc.tests'],
#       # package_data = {'pycnc' : files },
#       scripts=[], long_description="""Generates EMC2 GCode for simple 2.5D shapes""")

setup(
    name='pycnc',
    version=pycnc.get_version(),
    url='http://github.com/floatingpointstack/pycnc/',
    # download_url='https://github.com/floatingpointstack/pycnc/archive/1.0.zip',  # git tag would be required
    license='GPL v2',
    author='Guillaume Florent',
    test_suite='nose.collector',
    # install_requires=[],  # should be similar to requirements.txt but for setuptools and pypandoc
    author_email='florentsailing@gmail.com',
    description='2.5D CNC Python routines to generate GCode for simple geometries',
    long_description=long_description,
    packages=['pycnc', 'pycnc.examples', 'pycnc.utils', 'pycnc.tests'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
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
