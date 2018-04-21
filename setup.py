from setuptools import setup
import os

PACKAGE = "efweb"
NAME = "efweb"
DESCRIPTION = "An asynchronous REST service framework."
AUTHOR = "jsyj"
AUTHOR_EMAIL = "853934146@qq.com"
URL = "https://github.com/mikuh/efweb"
VERSION = __import__(PACKAGE).__version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.rst"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=["efweb"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    zip_safe=False,
    install_requires=[
            'aiohttp',
            'aiohttp_cors'
        ]
)