#!/usr/bin/env bash

# Bash uses dynamic scoping.
# Dynamic scoping means variable lookups
# occur in the scope where the function is
# called not where it is defined

function greetme() {
  if [ -n "$name" ]; then
    echo "Hello $name, how was your day?"
  else
    echo "I do not know who you are?"
    return 1
  fi
}

function sister() {
  local name="Faith Njeri"
  greetme
}

function brother() {
  local name="Simon Nganga"
  greetme
}

function mother() {
  local name="Lydia Njeri"
  greetme
}

function father() {
  local name="Charles Njroge"
  greetme
}

function maintest() {
  unset name
  sister # Hello Faith Njeri, how was your day?
  brother # Hello Simon Nganga, how was your day?
  mother # Hello Lydia Njeri, how was your day?
  father # Hello Charles Njoroge, how was your day?
  greetme # Error: I do not know who you are?
}

maintest