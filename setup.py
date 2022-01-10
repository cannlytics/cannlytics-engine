"""
Module Setup | Cannlytics Engine
Copyright (c) 2021-2022 Cannlytics

Authors: Keegan Skeate <keegan@cannlytics.com>
Contact: <keegan@cannlytics.com>
Created: 1/21/2021
Updated: 1/20/2022
License: MIT <https://opensource.org/licenses/MIT>
"""
from setuptools import find_packages, setup

# Get the project description.
README = ''
with open('README.md', 'r', encoding='utf-8') as readme_file:
    README = readme_file.read()

# Specify requirements installed by `pip install cannlytics`.
REQUIREMENTS = []
with open('requirements.txt', 'r') as f:
    REQUIREMENTS = [i[:-1] for i in f if i[0] != '#']

# Specify requirements for development.
dev_requirements = ['ocean-lib', 'xlwings']

# Specify requirements for setup.
setup_requirements = []

# Specify requirements for testing.
test_requirements = []

# Publish the module.
setup(
    author='Cannlytics',
    author_email='dev@cannlytics.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
    ],
    description='🔥 Cannlytics is simple, easy-to-use, end-to-end cannabis analytics software designed to make your data and information accessible.', #pylint: disable=line-too-long
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements + test_requirements,
    },
    include_package_data=True,
    install_requires=REQUIREMENTS,
    keywords='cannlytics',
    license='MIT',
    long_description=README,
    long_description_content_type='text/markdown',
    name='cannlytics',
    packages=find_packages(),
    python_requires='>=3.9',
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/cannlytics/cannlytics-engine',
    version='0.0.9',
    zip_safe=False,
)
