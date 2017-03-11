# coding: utf-8
import os
import re
import setuptools
import codecs

classes = """
    Development Status :: 3 - Alpha
    Environment :: Console
    Intended Audience :: Developers
    License :: OSI Approved :: MIT License
    Topic :: Terminals
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.5
    Programming Language :: Python :: 3.6
"""

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
    name='nutstore-cli',
    version=read('version'),
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    url='https://github.com/Kxrr/nutstore-cli',
    license='MIT',
    author='Kxrr',
    author_email='hi@kxrr.us',
    description='A command-line interface for NutStore based on WebDAV.',
    classifiers=[s.strip() for s in classes.split('\n') if s],
    install_requires=get_requirements(),
    include_package_data=True,
    dependency_links=['git+https://github.com/Kxrr/easywebdav.git#egg=easywebdav-1.2.2', ],
    entry_points={
        'console_scripts': [
            'nutstore-cli = nutstore_cli.__main__:main',
        ],

    },
)
