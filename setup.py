# -*- coding: utf-8 -*-
"""
setup.py | Cannlytics

Author: Keegan Skeate <keegan@cannlytics.com>
Contact: <keegan@cannlytics.com>
Created: 1/21/2021
Updated: 4/20/2021
License: GPLv3
"""
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='cannlytics',
    version='0.0.6',
    author='Cannlytics',
    author_email='contact@cannlytics.com',
    description='Cannlytics provides a user-friendly interface to quickly receive samples, perform analyses, collect and review results, and publish certificates of analysis (CoAs). There are also built in logistics, CRM (client relationship management), inventory management, and invoicing tools.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cannlytics/cannlytics-engine',
    packages=setuptools.find_packages(),
    license='GPLv3+',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        'beautifulsoup4',
        'django',
        'firebase_admin',
        'googlemaps',
        'pandas',
    ],
)
