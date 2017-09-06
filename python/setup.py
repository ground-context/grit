import sys
from setuptools import setup, find_packages

NAME="ground-client"
VERSION="0.1.2"
REQUIRES = ["requests >= 2.17.0"]

setup(
    name=NAME,
    version=VERSION,
    description="Python Ground API client",
    packages=find_packages(),
    include_package_date=True
)
