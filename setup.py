# -*- coding: utf-8 -*-
"""
setup.py | Cannlytics

Author: Keegan Skeate <keegan@cannlytics.com>
Contact: <keegan@cannlytics.com>
Created: 1/21/2021
Updated: 11/5/2021
License: MIT
"""
from setuptools import find_namespace_packages, setup

with open('README.md', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

# Possibly required by developers of cannlytics:
dev_requirements = []

# Installed by pip install ocean-lib
# or pip install -e .
install_requirements = [
    'beautifulsoup4',
    'django',
    'firebase_admin',
    'googlemaps',
    'pandas',
]

# Required to run setup.py:
setup_requirements = []

test_requirements = []

# Get packages.
packages = find_namespace_packages(include=['cannlytics'], exclude=['*test*'])

setup(
    author='Cannlytics',
    author_email='dev@cannlytics.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description='🔥 Cannlytics is simple, easy-to-use, end-to-end cannabis analytics software designed to make your data and information accessible.',
    extras_require={
        "test": test_requirements,
        "dev": dev_requirements + test_requirements,
    },
    include_package_data=True,
    install_requires=install_requirements,
    keywords='cannlytics',
    license='MIT',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='cannlytics',
    packages=packages,
    python_requires='>=3.8',
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/cannlytics/cannlytics-engine',
    version='0.0.9',
    zip_safe=False,
)
