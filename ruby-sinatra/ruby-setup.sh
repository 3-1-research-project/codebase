#!/bin/sh

RUBY_VERSION=3.4.0

apt install -y \
    libpq-dev \
    build-essential \
    ca-certificates \
    curl \
    libz-dev \
    libffi-dev \
    libedit-dev \
    libyaml-dev \
    rbenv \
    ruby \
    ruby-dev 

# Install allocators
apt install -y \
    libjemalloc2 

apt install rbenv

git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build

eval "$(rbenv init -)"

# rbenv install $RUBY_VERSION

# rbenv global $RUBY_VERSION
# rbenv local $RUBY_VERSION
# rbenv shell $RUBY_VERSION
# rbenv rehash
