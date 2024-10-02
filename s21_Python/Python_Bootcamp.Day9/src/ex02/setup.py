from setuptools import setup
from Cython.Build import cythonize

setup(
    name="cyth",
    ext_modules=cythonize("cyth/multiply.pyx"),
    zip_safe=False,
)
