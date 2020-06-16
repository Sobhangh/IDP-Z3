from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(["Idp/Substitute.pyx"], annotate=True, language_level=3),
    zip_safe=False,
)