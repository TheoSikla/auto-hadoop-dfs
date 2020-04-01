#!/bin/bash

# Donwload and install pyenv
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

## Install necessary dependencies
#apt-get install -y make build-essential libssl-dev zlib1g-dev \
#libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
#libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl

if ! grep -q pyenv "$HOME/.bashrc"; then
  echo '
export PATH="/home/$USER//.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
' >> "$HOME/.bashrc"
fi

export PATH="/home/$USER//.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install Python 3.7.0
pyenv install -v 3.7.0

# List available Python versions in pyenv
# ls ~/.pyenv/versions/ or pyenv versions

# Uninstall a Python version from pyenv
# rm -rf ~/.pyenv/versions/3.7.0 or pyenv uninstall 2.7.15

# View current global Python version
# python -V

# View current pip used
# pyenv which pip

# Set Python 3.7.0 as global
pyenv global 3.7.0

# Install pipenv
pip install pipenv
