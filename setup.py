#!/usr/bin/env python

from setuptools import setup, find_packages
from bigone import VERSION

url="https://github.com/jeffkit/bigone-python/"

long_description="Python SDK for Big.One (https://big.one)"

setup(name="bigone",
      version=VERSION,
      description=long_description,
      maintainer="jeff kit",
      maintainer_email="jeffkit.info@gmail.com",
      url = url,
      long_description=long_description,
      install_requires = ['requests', 'pyjwt'],
      packages=find_packages('.'),
     )
