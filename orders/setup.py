#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='nameko-orderService',
    version='0.0.1',
    description='Store and serve orders',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        'nameko==2.14.0',
        'pymysql==0.9.3',
        'marshmallow==3.5.1',
        'redis==3.4.1',
    ],
    extras_require={
        'dev': [
            'pytest==4.5.0',
            'coverage==4.5.3',
            'flake8==3.7.7',
        ],
    },
    zip_safe=True
)
