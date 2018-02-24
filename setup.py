from setuptools import setup, find_packages
setup(
    name='pythoncommons',
    packages=find_packages(),
    include_package_data=True,
    version='0.0.1',
    description='Generic utilities for MARS and Harness projects.',
    author='Ryan Berkheimer',
    author_email='rab25@case.edu',
    url='https://github.com/RBerkheimer/pythoncommons',
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic"])
