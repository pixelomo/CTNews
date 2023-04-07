# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'CTNews',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = articles.settings']},
)
