# coding: utf-8
import os

from setuptools import setup, find_packages

import lbc_scraper

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()
with open(os.path.join(here, 'requirements.txt')) as f:
    REQUIRES = f.read()


setup(
    name='lbc_scraper',
    version=lbc_scraper.__version__,
    description='',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Marion Delcambre',
    author_email='delcambremarion@gmail.com',
    keywords='lbc leboncoin alert scraper',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRES,
    entry_points = {
        'console_scripts': [
            'lbc-scraper = lbc_scraper.main:start_scraper',
        ],
    }
)
