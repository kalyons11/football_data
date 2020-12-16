"""
Package setup file.
"""

import sys
from setuptools import setup, find_packages

sys.path.append('pfr_functions/')
from __init__ import __version__, __author__, __description__

setup(name='pfr_functions',
      version=__version__,
      author=__author__,
      description=__description__,
      url='hhttps://github.com/kalyons11/football_data',
      author_email='kevinandrewlyons@gmail.com',
      license='MIT',
      packages=find_packages()
      )
