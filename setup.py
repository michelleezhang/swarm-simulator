from importlib.metadata import entry_points
from setuptools import find_packages
from setuptools import setup

setup(
    name='sim_pkg',
    version='2.0',
    description='Swarm simulator',
    author='Michelle Zhang',
    author_email='michellezhang2024@u.northwestern.edu',
    url='',
    packages=find_packages(),
    entry_points={'console_scripts':['swarm_simulator = sim_pkg.run:main'],},
)