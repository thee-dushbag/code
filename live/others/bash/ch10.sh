#!/usr/bin/env bash

# Control Structures.
## File Operations.
function pathtype() {
  for path; do
    if [ -e "$path" ]; then
      echo "PathFound: '$path'"
      if [ -h "$path" ]; then
        echo "  - Link Path"
        if [ -f "$(realpath "$path")" ]; then
          echo "    - File Link"
        fi
        if [ -d "$(realpath "$path")" ]; then
          echo "    - Directory Link"
        fi
      elif [ -f "$path" ]; then
        echo "  - File Path"
      elif [ -d "$path" ]; then
        echo "  - Directory Path"
      else
        echo "  - Unknown file type"
      fi
    else
      echo "PathNotFound: '$path'"
    fi
  done
}

function ifblock() {
  # Example of If statement in Bash
  # The square bracket is no part of the syntax,
  # it is being treated as a command and its exit
  # code is all that matters, 0 for true, others for false.
  if [ $1 -eq 1 ]; then
    # If-Block
    echo 'You passed Number 1'
  elif [ $1 -gt 1 ]; then
    # Else-If-Block
    echo 'You passed a Number > 1'
  else
    # Else-Block
    echo 'Youe passed a Number < 1'
  fi
  # Syntax:
  # if command --arg uments; then
  #   # Commands to execute on true
  # fi # End of block
  # Also mathematical expressions can be the command
  # if (( $1 < 7 * $2 )); then <do something>; fi
}

function looping() {
  # Define an array
  local vowels=(a e i o u)
  local i=0
  # Using a for loop
  # Looping over each of them
  echo "Iterating using a for loop."
  for vowel in ${vowels[@]}; do
    echo "F-Vowel: $vowel"
  done
  # Or C-Style for loop
  for ((i = 0; i < ${#vowels[@]}; i++)); do
    echo "F-CVowel: ${vowels[$i]}"
  done
  echo "Iterating using a while loop."
  i=0
  while [ $i -lt ${#vowels[@]} ]; do
    echo "W-Vowel: ${vowels[$i]}"
    i=$(($i + 1))
    # Or
    # i=$(expr $i + 1)
  done
  i=0
  while (($i < ${#vowels[@]})); do
    echo "W-CVowel: ${vowels[$i]}"
    ((i++))
  done
  # You can also iterate over a list of values
  echo "Iterate over a list of values."
  for number in 1 2 3 4 5; do echo Number: $number; done
  # Also similar to using brace expansion
  # for number in {1..5}; do echo Number: $number; done
}

function contbr() {
  echo Break once we reach a number greater than 4.
  for number in {1..10}; do
    echo Current: $number
    if [ $number -gt 4 ]; then
      echo Breaking
      break
    fi
  done
  echo Skip operation on 4.
  for number in {1..10}; do
    if [ $number -eq 4 ]; then
      echo Skipping 4.
      continue
    fi
    echo Current: $number
  done
  echo Breaking a nested loop.
  for n in {1..4}; do
    for m in {1..4}; do
      if [ $m -eq 3 ]; then break 2; fi
      echo Current: n=$n, m=$m
    done
    echo
  done
}

function _ispint_impl() {
  for arg; do [[ $arg =~ ^[0-9]+$ ]] || return 1; done
}

function _usaflag_impl() {
  local width="$1"
  local height="$2"
  local h=$(expr $height / 2)
  local w=$(expr $width / 2)

  for i in $(seq $height); do
    for j in $(seq $width); do
      if [ $j -le $w ] && [ $i -le $h ]; then
        echo -n '*'
      else
        echo -n '-'
      fi
    done
    echo
  done
}

function usaflag() {
  local _h=8 _w=30 # Default Values
  while [ $# -ne 0 ]; do
    case "$1" in
    --help | -H)
      echo Usage for: $FUNCNAME
      echo Options:
      echo "  --help   -H             print this message and exit."
      echo "  --width  -w <number>    Width of the flag."
      echo "  --height -h <number>    Height of the flag."
      echo "Example: $FUNCNAME -w 40 -h 20"
      return 0
      ;;
    --height | -h)
      if [ -z "$2" ]; then
        echo >&2 'Expected a number for height. In -h/--height flag.'
        return 1
      fi
      _h="$2"
      ;;
    --width | -w)
      if [ -z "$2" ]; then
        echo >&2 'Expected a number for width. In -w/--width flag.'
        return 1
      fi
      _w="$2"
      ;;
    *)
      echo >&2 Unexpected Parameter: \'$1\'
      return 1
      ;;
    esac
    shift 2
  done
  if ! _ispint_impl "$_h" "$_w" &>/dev/null; then
    echo >&2 Expected integers for width and height. Need help:
    echo >&2 "  $FUNCNAME --help"
    return 1
  fi
  _usaflag_impl "$_w" "$_h"
}

function octrlstruct() {
  # Until Loop
  # Switch Statement
  echo Until loop executes until given condition is True.
  local counter=10
  until [ $counter -eq 3 ]; do
    echo Current Value: $counter
    ((counter--))
  done
  case $1 in
  simon)
    echo Your name is Simon
    ;;
  nganga)
    echo Your name is Nganga
    ;;
  njoroge)
    echo Your name is Njoroge
    ;;
  *)
    echo I do not know your name, $1
    ;;
  esac
}

function opts() {
  local name=()
  local bye=()
  local greet=()
  local hosts=()
  local ports=()
  while [ $# -ne 0 ]; do
    case $1 in
    --help | -h)
      echo -e '--help  -h Display this help and exit\n--name  -n Pass in your name\n--bind  -b Bind to some host port address\n--greet -g Person to greet\n--bye   -y Say Goodbye to person'
      return 0
      ;;
    --name | -n)
      name+=("$2")
      shift 2
      ;;
    --greet | -g)
      greet+=("$2")
      shift 2
      ;;
    --bind | -b)
      hosts+=("$2")
      ports+=("$3")
      shift 3
      ;;
    --bye | -y)
      bye+=("$2")
      shift 2
      ;;
    *)
      echo Unrecognized option: $1 >&2
      return 1
      ;;
    esac
  done
  echo Names:
  for name in "${name[@]}"; do
    echo "  - $name"
  done

  echo Bye:
  for name in "${bye[@]}"; do
    echo "  - $name"
  done

  echo Greet:
  for name in "${greet[@]}"; do
    echo "  - $name"
  done

  echo Locations:
  for ((i = 0; i < ${#hosts[@]}; i++)); do
    echo "  - Host: ${hosts[$i]} | Port: ${ports[$i]}"
  done
}

function argloop() {
  # This is a for loop that iterates over the
  # arguments passed its holder, eg a function or module.
  # Normally a for loop written as
  # for arg in "$@"; do :; done
  # this can be shortened to
  # for arg; do :; done
  echo Args:
  # for arg in "$@"; do echo "  - $arg"; done
  for arg; do echo "  - $arg"; done
}

# function _trap2() {
#   echo -e \nBreaking Loop.
# }
# trap _trap2 SIGINT

function tfcolon() {
  # The colon is a special builtin command that
  # is used in places where a command is required
  # but there is none to be given. It is used in the
  # then block of if statements to act as a place
  # holder for a command. The :(colon) command does
  # nothing and simply returns an exit status of 0.
  # Each colon below represents a command substitution point.
  if :; then :; else :; fi

  # true and false are executable files in
  # PATH. true simply exists with a 0 while false
  # exists with 1 exit code.
  # Creating Infinite Loops
  echo Infinite loop with while.
  local counter=1
  while true; do
    echo -en "\r[While] Counter: $counter"
    ((counter++))
    sleep 0.2s
  done
  echo

  echo Infinite loop with until.
  counter=1
  until false; do
    echo -en "\r[Until] Counter: $counter"
    ((counter++))
    sleep 0.2s
  done
  echo
}
