from setuptools import setup, find_packages
setup(
    name='pythoncommons',
    packages=find_packages(),
    install_requires=[
        'simplejson',
        'pymongo',
        'bson',
        'geojson'
    ]
    include_package_data=True,
    version='0.0.1',
    description='Generic, behavior grouped python utilities.',
    author='Ryan Berkheimer',
    author_email='rab25@case.edu',
    url='https://github.com/RBerkheimer/pythoncommons',
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: MIT Standard",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic"])
