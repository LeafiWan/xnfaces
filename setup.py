#!/usr/bin/env python
#coding=utf-8

from setuptools import setup, find_packages

name = "xnfaces"
version = "0.1"
license = 'WTFPL'
description = "Facemash-like site for Xiangnan University.",
author = 'lope'

install_requires = ["flask>=0.9",
                    ]

entry_points = """
[console_scripts]
    run_web = xnfaces.web:main
"""

setup(name=name,
      version=version,
      license=license,
      description=description,
      author=author,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=install_requires,
      entry_points=entry_points)
