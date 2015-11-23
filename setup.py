import os
from setuptools import setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
README = (
    open(os.path.join(BASE_DIR, 'README.md')).read()
)

setup(
    name='sphinx-confluence',
    description='Atlassian Confluence extension for sphinx',
    long_description=README,
    version='0.0.2',
    author='Arello Mobile',
    url='https://github.com/Arello-Mobile/sphinx-confluence',
    packages=['sphinx_confluence'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)