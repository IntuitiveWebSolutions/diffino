import os
from setuptools import setup

VERSION = "0.1.8"

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="diffino",
    version=VERSION,
    packages=["diffino"],
    include_package_data=True,
    install_requires=[
        "pandas==0.19.2",
        "boto3==1.9.151"
    ],
    entry_points={'console_scripts': ['diffino = diffino.cli:main']},
    author="BriteCore",
    description="Diffing tools for comparing datasets in CSV, XLSX and other formats",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    keywords="diffing comparing csv excel json",
    url="https://github.com/IntuitiveWebSolutions/diffino"
)
