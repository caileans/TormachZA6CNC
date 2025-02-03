#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

setup_args = generate_distutils_setup(
     packages=['preProcessing'],
     package_dir={'': '../../..'}
)

setup(**setup_args)

setup_args = generate_distutils_setup(
     packages=['lib'],
     package_dir={'': 'scripts'}
)

setup(**setup_args)

