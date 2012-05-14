##############################################################################
#
# Copyright (c) 2012, 2degrees Limited <gustavonarea@2degreesnetwork.com>.
# All Rights Reserved.
#
# This file is part of wsgi-lag <https://github.com/2degrees/wsgi-lag>,
# which is subject to the provisions of the BSD at
# <http://dev.2degreesnetwork.com/p/2degrees-license.html>. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED "AS IS"
# AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST
# INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os

from setuptools import setup, find_packages

_branch_path = os.path.abspath(os.path.dirname(__file__))
_readme = open(os.path.join(_branch_path, 'README.txt')).read()
_version = open(os.path.join(_branch_path, 'VERSION.txt')).readline().rstrip()


setup(
    name='wsgi-lag',
    version=_version,
    description='WSGI middleware to report on the time lag between requests ' \
        'and their respective responses',
    long_description=_readme,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        ],
    keywords='web performance',
    author='2degrees Limited',
    author_email='2degrees-floss@googlegroups.com',
    url='http://packages.python.org/wsgi-lag/',
    license='BSD (http://dev.2degreesnetwork.com/p/2degrees-license.html)',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    tests_require = ['coverage', 'nose'],
    test_suite='nose.collector',
    )
