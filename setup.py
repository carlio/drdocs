# -*- coding: utf-8 -*-
import os
from distutils.core import setup

from setuptools import find_packages

_version = "0.1"
_packages = find_packages('drdocs', exclude=["*.tests", "*.tests.*", "tests.*", "tests"])


def _strip_comments(line):
    return line.split('#', 1)[0].strip()


def _get_reqs():
    reqs_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(reqs_file) as f:
        requires = f.readlines()
        requires = map(_strip_comments, requires)
        requires = filter(lambda x: x.strip() != '', requires)
        return requires


_CLASSIFIERS = (
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Operating System :: Unix',
    'Topic :: Software Development :: Quality Assurance',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: '
    'GNU General Public License v2 or later (GPLv2+)',
)


setup(
    classifiers=_CLASSIFIERS,
    name='drdocs',
    version=_version,

    packages=_packages,
    package_dir={'': 'drdocs'},

    description="Python tool to measure documentation coverage",
    # long_description='',
    license='GPLv2',
    zip_safe=False,

    install_requires=_get_reqs(),

    data_files=[('', ['requirements.txt']), ],
    entry_points={
        'console_scripts': [
            'drdocs = drdocs.entry:run',
        ],
    },
)
