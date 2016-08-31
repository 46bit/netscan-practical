'''
Setup file for cp_ftp

@author: Howard Chivers

Copyright (c) 2015, Howard Chivers
All rights reserved.
'''

from setuptools import setup

setup(
    name='cp_ftp',

    version='0.1.0',

    description='cp_ftp FTP exploit library',

    author='Michael Mokrysz',
    author_email='mm911@york.ac.uk',
    url="https://www.cs.york.ac.uk/cyber-practicals/",

    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3',
                 'Topic :: Scientific/Engineering :: Information Analysis',
                 'Topic :: Security',
                 ],

    install_requires=[],

    keywords='ftp education',

    packages=['cp_ftp'],
    package_dir={'cp_ftp': 'cp_ftp'},
    entry_points={},
    package_data={}
)
