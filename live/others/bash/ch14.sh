#!/usr/bin/env bash
# Learning bash Function and parameter expansion

function str.upper() {
  declare -u ustr="$*"
  echo "$ustr"
}

function str.lower() {
  declare -l lstr="$*"
  echo "$lstr"
}

function _title_word_impl() {
  local word="$1"
  echo "$(str.upper "${word:0:1}")$(str.lower "${word:1}")"
}

function str.title() {
  local words
  for sentence; do
    words=()
    for word in $sentence; do
      words+=($(_title_word_impl "$word"))
    done
    echo "${words[*]}"
  done
}

# To set a default value to a variable if one was not passed
# use: echo ${name:-anonymous}

function _greet_impl() {
  echo "Hello $(str.title "${1:-anonymous}"), how was your day?"
}

function greet() {
  for name; do
    _greet_impl "$name"
  done
}

function getfunc() {
  declare -f "$@"
}

# Functions that support named parameters can be achieved by
# using the case...esac control structure to retrieve the values.
# Example

function namedparam() {
  . ./ch10.sh
  opts "$@"
}