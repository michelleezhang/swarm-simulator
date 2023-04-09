#!/usr/bin/bash

# First update system
sudo apt install wget
sudo apt update
sudo apt upgrade -y

# I believe that right now, swarm-sim
# python2: typing numpy
# python3: pygame pandas
sudo apt install python3 -y
sudo apt install python2 -y
sudo apt install python-pip -y
pip2 install typing
pip2 install numpy

# This will install miniconda in the home directory
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh -O miniconda_installer.sh
chmod +x ./miniconda_installer.sh
./miniconda_installer.sh
echo '. "$HOME/miniconda3/etc/profile.d/conda.sh"' >> ~/.bashrc
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc

# Source bashrc after installing stuff to path
source $HOME/.bashrc

$HOME/miniconda3/bin/conda create python=3.10 pandas pygame -n swarm_sim_env -c conda-forge

# After this, just run:
# ```
#     conda activate swarm_sim_env 
# ```
