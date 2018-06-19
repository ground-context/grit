from setuptools import setup, find_packages

NAME = "grit-backend"
VERSION = "0.0.1"
REQUIRES = ["requests >= 2.17.0"]

setup(
    name=NAME,
    version=VERSION,
    description="Python Ground on Git Implementation",
    packages=find_packages(),
    install_requires=REQUIRES,
    include_package_date=True
)
