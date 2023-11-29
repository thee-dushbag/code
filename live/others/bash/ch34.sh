#!/usr/bin/env bash

# Reading on Bash Pattern Matching.

function regex1() {
  local a="I am a simple string with digits 1234"
  local pat="(.*) ([0-9]+)"
  [[ "$a" =~ $pat ]]
  echo "Whole match: '${BASH_REMATCH[0]}'"
  echo "First group: '${BASH_REMATCH[1]}'"
  echo "Second group: '${BASH_REMATCH[2]}'"
}

function ubonnomatch() {
  # prepare an environment
  local env_dir="$(mktemp -d)"
  cd "$env_dir"
  local shoptstate="$(shopt -p)"
  shopt -u nullglob failglob dotglob nocaseglob extglob globstar
  $shoptstate
  rm -rf "$env_dir"
}

regex1