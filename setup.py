#!/usr/bin/env python
# -*- coding: utf-8 -*-

import versioneer
import sys

from setuptools import setup

with open('README.rst', 'r') as fp:
    readme = fp.read()

with open('HISTORY.rst', 'r') as fp:
    history = fp.read().replace('.. :changelog:', '')

with open('requirements.txt', 'r') as fp:
    requirements = list(filter(bool, (line.strip() for line in fp)))

with open('requirements-dev.txt', 'r') as fp:
    dev_requirements = list(filter(bool, (line.strip() for line in fp)))

# Require pytest-runner only when running tests
pytest_runner = (['pytest-runner>=2.0,<3dev']
                 if any(arg in sys.argv for arg in ('pytest', 'test'))
                 else [])

setup_requires = pytest_runner

setup(
    name='scikit-ci-addons',

    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    author='The scikit-build team',
    author_email='scikit-build@googlegroups.com',

    url='https://github.com/scikit-build/scikit-ci-addons',

    description='scikit-ci-addons is a set of scripts useful to easily install selected'
                ' software packages as well as helping drive the CI of projects leveraging'
                ' services like CircleCI, or TravisCI.',
    long_description=readme + '\n\n' + history,

    entry_points={'console_scripts': ['ci_addons=ci_addons.__main__:main']},

    packages=['anyci', 'ci_addons', 'circle', 'travis', 'windows'],
    include_package_data=True,
    zip_safe=False,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Build Tools'
    ],

    license="Apache",

    keywords='CI CircleCI Travis',

    setup_requires=setup_requires,
    install_requires=requirements,
    tests_require=dev_requirements,
)
