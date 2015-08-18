from setuptools import setup, find_packages  # Always prefer setuptools over distutils

setup(
    name = 'scikit-extremes',
    version = '0.0.1',
    description = 'Library to perform univariate extreme value analysis',
    long_description = '''scikit-extremes
===============

Library to perform univariate extreme value analysis''',
    url = 'https://github.com/kikocorreoso/scikit-extremes',
    author = 'Kiko Correoso',
    author_email = '',
    license = 'MIT',
    classifiers = '''Development Status :: 3 - Alpha
Topic :: Statistics :: EVT :: Extreme value theory :: EVA :: Extreme value analysis
License :: MIT License
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4''',
    keywords = 'statistics extremes EVT EVA',
    packages = find_packages(exclude=['tests']),
    install_requires = ['numpy', 'matplotlib', 'scipy', 'numdifftools'],
    extras_require = {},
    package_data={
    'datasets': ['*.csv']
},
    entry_points={
    'console_scripts': [
        'sample=sample:main',
    ]
},
)
