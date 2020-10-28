#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
 
setup(
    name='PowerControl',# 此处填写包名
    version='0.0.1',
    author='liuchengyiu',
    author_email='liuchengyiu@163.com',
    description='this project is for powercontrol test',
    license='PRIVATE',
    package_dir = {'':'power_control_test'},
    install_requires = [
        'psutil>=2.10.5'
    ]
)