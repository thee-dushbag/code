#!/usr/bin/env bash

function word_spliting() {
  set -x
  local var='I am
a
multiline string'
  function fun() {
    echo "-$1-"
    echo "*$2*"
    echo ".$3."
  }
  fun $var # <- will be broken into multiple
  # arguments from the newlines and spaces.
}

function read_names() {
  local names="Simon:Nganga:Njoroge:"
  IFS=:
  while read -d: name; do
    echo Name: $name
  done <<<$names
}

# To register a cleanup function on exit
# use the SIGEXIT which is thrown by must
# every time a program exits.

function longtime() {
  echo PID: $$ # print this script's process id
  sleep 10
}

trap 'echo SigTERM caught && exit' TERM
trap 'echo SigCONT caught && exit' CONT
trap 'echo SigINT caught && exit' INT

longtime

# Trap command: trap <command> <signals...>
# Example: trap ls INT KILL TERM


# read_names
# word_spliting
