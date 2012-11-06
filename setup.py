#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup

from torelp import __version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='torelp',
    version=__version__,
    author='Shane R. Spencer',
    author_email='shane@bogomip.com',
    packages=['torelp'],
    url='https://github.com/whardier/torelp',
    license='MIT',
    description='Tornado based RELP server (standard and inetd sockets)',
    long_description=read('README'),
    install_requires=[
        'tornado>=2.4',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: No Input/Output (Daemon)',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
)


