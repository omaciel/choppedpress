# -*- encoding: utf-8 -*-
# vim: ts=4 sw=4 expandtab ai

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

from setuptools import setup, find_packages

setup(
        name = "choppedpress",
        version = "0.0.1",
        description = "Split WordPress XML export files into smaller files to import into a new WordPress installations.",
        long_description = readme,
        author = "Og Maciel",
        author_email = "omaciel@ogmaciel.com",
        url="http://omaciel.github.com/choppedpress/",
        license = license,
        packages = find_packages(exclude=('tests', 'docs',)),
        scripts = ['choppedpress',]
        )
