#!/usr/bin/env bash

# File execution sequence

# Files:
# 1) .bash_profile
# 2) .bash_login
# 3) .profile
# 4) .bashrc

# Used to set up and define functions, variables and the sorts
# Difference: .bashrc is called at the opening of a non-login
# but interactive window while .bash_profile and the others are
# called for a login shell.

# Splitting files

function random_text() {
  local -i count="${1:-5}" _cur
  for _cur in $(seq $count); do
    echo -n "$(($RANDOM * _cur))" | sha512sum
  done
}

function prepare_split() {
  local file="ignore/random_text"
  if [ ! -f "$file" ]; then
    mkdir -p ignore
    echo "Preparing for split test..."
    random_text 15000 >"$file"
    echo "Created test file $file..."
  fi
}

function cleanup_split() {
  rm -rfv ignore
}

function split_random_text_file() {
  # prepare_split
  local file="ignore/random_text"
  split "$file"
  # cleanup_split
}
