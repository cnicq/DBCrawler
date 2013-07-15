from setuptools import setup, find_packages

setup(
    name='DBCrawler',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy': ['settings = DBCrawler.settings']},
)
