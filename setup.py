import os
from setuptools import setup

long_description = open('README.rst' if os.path.exists('README.rst') else 'README.md').read()

setup(
    name='sphinx-confluence',
    description='Atlassian Confluence extension for sphinx',
    long_description=long_description,
    version='0.0.3',
    author='Arello Mobile',
    url='https://github.com/Arello-Mobile/sphinx-confluence',
    packages=['sphinx_confluence'],
    include_package_data=True,
    license='MIT',
    install_requires=open('requirements.txt').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
