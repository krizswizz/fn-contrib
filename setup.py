import os
import sys
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

required_version = (3, 3)
if sys.version_info < required_version:
    raise SystemExit('Fn.py-contrib requires Python {}'.format(
        '.'.join(map(str, required_version))))

setup(
    name='fncontrib',
    version='0.0.0',
    description='Underscore-contrib inspired FP library',
    author='Alain Péteut',
    platform='all'
)
