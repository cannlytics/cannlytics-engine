# -*- coding: utf-8 -*-
"""
setup.py | cannlytics
Copyright © 2021 Cannlytics
Author: Keegan Skeate <keegan@cannlytics.com>
Created: 1/21/2021
Updated: 3/18/2021

License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cannlytics",
    version="0.0.6",
    author="Cannlytics",
    author_email="contact@cannlytics.com",
    description="Cannlytics provides a user-friendly interface to quickly receive samples, perform analyses, collect and review results, and publish certificates of analysis (CoAs). There are also built in logistics, CRM (client relationship management), inventory management, and invoicing tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cannlytics/cannlytics-engine",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    install_requires=[
        "beautifulsoup4",
        "django",
        "firebase_admin",
        "googlemaps",
        "pandas",
    ],
)
