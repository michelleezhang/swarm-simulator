from setuptools import setup, find_packages

setup(
    name='sim_pkg',
    version='2.0',
    description='Swarm simulator package',
    author='Michelle Zhang',
    author_email='michellezhang2024@u.northwestern.edu',
    url='',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.0',
        'matplotlib>=3.7', 
        'pygame>=2.5',
    ],
    entry_points={'console_scripts':['swarm_simulator = sim_pkg.coachbot_simulator:main'],}, # CHANGED FROM BELOW
    # entry_points={'console_scripts':['swarm_simulator = sim_pkg.run:main'],},
)