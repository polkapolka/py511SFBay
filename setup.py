"""\
This setup.py was provided by `package`, the Python package package package.

See http://pypi.python.org/pypi/package/ for more information.
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py511SFBay',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='511 RTD API.  Use it to Flee your home or work. Why flee? Leave was already taken.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/polkapolka/py511SFBay',

    # Author details
    author='Polka',
    author_email='ph.ebe.po.lk@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='VTA Tri Delta Transit Santa Rosa CityBus BART SamTrans AC Transit Marin Transit Vine (Napa County) Dumbarton Express WESTCAT SF-MUNI County Connection LAVTA Caltrain real time departures 511 transit',

    # What is required for this package?
    install_requires = [
    #     'curses',
        'pymsgbox',
        'argparse',
        'requests',
        # 'textwrap',
        # 'xml.etree.ElementTree',
        # 'json',
        # 're',
        # 'errno'
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'flee=py511SFBay.main:main',
        ],
    },
)