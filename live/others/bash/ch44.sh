#!/usr/bin/env bash

function _path_env() {
  # The path environment variable
  # holds the sources where an executable
  # for a command will be found. It contains
  # a list of colon separated paths.
  local -i cnt=1
  echo PATH:
  while read -d: path; do
    echo '  ' $cnt $path
    ((cnt++))
  done <<<"$PATH"
  # To add a path to PATH just concat it
  # with the previous PATH having a colon
  # between them
  local path="$(realpath ./bin)"
  local command="hello Simon Faith"
  echo "hello command can be found at: '$path'"
  echo "Running hello before adding path to PATH"
  $command
  PATH=$path:$PATH
  echo "Adding path to PATH. Retrying hello command"
  $command
  # Note that once we exit this script, our
  # PATH modification will be lost and the hello
  # command cannot be found again from the callers 
  # context. To make it permanent, add the custom
  # path in your launcher script .bashrc
}

function remove_path() {
  local path_pattern
  for path; do
    path_pattern="(.*:)?$path(:.*)?"
    if [[ "$PATH" =~ $path_pattern ]]; then
      PATH="${BASH_REMATCH[1]}:${BASH_REMATCH[2]}"
      PATH="${PATH/:::/:}"
      PATH="${PATH/::/:}"
    fi
  done
  PATH="${PATH#:*}"
  PATH="${PATH%*:}"
}

function add_paths() {
  # PATH="${*/ /:}"
  for path; do
    PATH="$path:$PATH"
  done
}

function test_rpath() {
  local -a paths=(~ ~/Content ~/.local)
  # echo "ToAdd: ${paths[c*]}"
  echo "OldPath: $PATH"
  add_paths "${paths[@]}"
  echo "NewPath: $PATH"
  remove_path "${paths[@]}"
  echo "DelPath: $PATH"
}

# _path_env
# test_rpath
