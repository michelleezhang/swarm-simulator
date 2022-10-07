from importlib.metadata import entry_points
from setuptools import find_packages
from setuptools import setup

setup(
    name='sim_pkg',
    version='1.0',
    description='',
    author='Devesh Bhura',
    author_email='deveshbhura2023@u.northwestern.edu',
    url='',
    packages=find_packages(),
    entry_points={'console_scripts':['swarm_simulator = sim_pkg.run:main'],},
)