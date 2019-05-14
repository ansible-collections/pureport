# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='pureport-ansible-modules',
    version='0.0.3',
    author='Pureport',
    author_email='noreply@pureport.com',
    license='GPLv3',
    description='Ansible modules to interact with the Pureport ReST API',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/pureport/pureport-ansible-modules',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
    ]
)
