#!/usr/bin/env bash

# Bash Internal Variables

function bash_arguments() {
  # $* -> "$1 $2 $3 $4 $5"
  # $@ -> "$1" "$2" "$3" "$4" "$5"
  # $# -> number of arguments to the script/function
  # $? -> exit status of the last command
  # ${n} -> nth positional argument, also written as $n for 0-9
  # $0 -> name of the script running
  # $IFS -> internal field separator
  # $PATH -> paths where executables can be found
  # $OLDPWD -> Previous working directory
  # $PWD -> Present working directory
  # $FUNCNAME -> Array of function names in the execution stack.
  # $BASH_SOURCE -> Array containing source paths for elements in FUNCNAME array.
  # $BASH_ALIASES -> Associative array containing all currently defined aliases
  # Arguments are separated by IFS which doesn't have to be a space
  :
}

function func_four() { echo "Four: ${FUNCNAME[@]}"; }
function func_three() {
  echo "Three: ${FUNCNAME[@]}"
  func_four
}
function func_two() {
  echo "Two: ${FUNCNAME[@]}"
  func_three
}
function func_one() {
  echo "One: ${FUNCNAME[@]}"
  func_two
}

function seefuncs() {
  echo "SeeFuncs: ${FUNCNAME[@]}"
  func_one
}

# seefuncs

# bash_arguments "$@"
