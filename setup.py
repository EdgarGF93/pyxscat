import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    include_package_data=True,
    name = "PyXScat",
    version = "0.1",
    author = "Edgar Gutierrez Fernandez",
    packages = find_packages(),
    author_email = "edgar.gutierrez-fernandez@esrf.fr",
    description = (""),
    license = "",
    keywords = "visualization browsing reduction pygix pyFAI",
    # url = "https://gitlab.esrf.fr/xmas-bm28/pyxscat/pyxscat",
    long_description=read('README.md'),
    install_requires=[
        'PyYAML',
        'pandas',
        'numpy',
        'matplotlib',
        'jupyter',
        'pygix',
        'pyFAI',
        'PyQt5',
    ]
)
