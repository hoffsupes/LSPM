
#
# ################################################################################
#   ## Copyright (C) Gaurav Dass - All Rights Reserved
#   ## Unauthorized copying of this file, via any medium is strictly prohibited
#   ## Proprietary and confidential
#   ## Written by Gaurav Dass <dassgaurav93@gmail.com>, January 2020
#
# ################################################################################

import setuptools
import sys
sys.path.append('..')
with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Large Scale Causal Relation Extraction", # Replace with your own username
    version="3.0.0",
    author="Gaurav Dass",
    author_email="dassgaurav93@gmail.com",
    description="Extract cause effect pairs from a large set of data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CISL-commons-SPA/LSPM",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
