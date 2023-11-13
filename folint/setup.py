import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="folint",
    version="1.0.8",
    description="Linter for FO-dot, used in the IDP-Z3 system",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/EAVISE/sva/folint",
    author="vadevesi",
    author_email="s.vandevelde@kuleuven.be",
    classifiers=[
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Software Development :: Quality Assurance'
      ],
    packages=find_packages(),
    install_requires=["idp_engine>=0.10.12"],
    entry_points={
      'console_scripts': ['folint=folint.SCA:main']
    }
)
