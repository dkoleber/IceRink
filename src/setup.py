from distutils.core import setup
from Cython.Build import cythonize
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))
HERE = os.path.dirname(os.path.abspath(__file__))

setup(
    ext_modules = cythonize(os.path.join(HERE,"Engine.pyx"))
)


