# coding: utf-8
import os
import re
import setuptools
import codecs


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'nutstore_cli', '__init__.py')) as f:
    META_CONTENT = f.read()


def read(variable):
    m = re.search('__%s__\s*=\s*[\'\"](\S*)[\'\"]$' % variable, META_CONTENT, flags=re.M)
    return m.group(1)


def get_requirements():
    reqs = codecs.open(os.path.join(here, 'requirements.txt'), encoding='utf-8').read().splitlines()
    return [req for req in reqs if not req.startswith('-e')]


setuptools.setup(
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    setup_requires=['pbr'],
    pbr=True,
)
