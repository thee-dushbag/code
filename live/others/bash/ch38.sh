#!/usr/bin/env bash

# Simple case statement

function simple_case() {
  # Simplest case that shorts when a match is
  # made.
  local var
  read -n 1 -p "Location level[int]: " var
  echo
  case "$var" in
  1) echo "[$var]: Location JKUAT" ;;
  2) echo "[$var]: Location Nairobi" ;;
  3) echo "[$var]: Location Kenya" ;;
  *) echo "[$var]: Invalid level, try 1, 2, 3." ;;
  esac
}

function case_wfallt_iff() {
  # Using the operator ;;&, this tells bash
  # to continue matching the next patterns
  # if and only if they match unitl it encounters
  # ;; or end of case statement
  local fruits
  local -a toeat
  local -A options=([a]=Apple [b]=Blueberry [c]=Cactus [d]=Donuts [e]=Eggplant)
  read -p "Fruits to eat: " fruits
  if [[ ! "$fruits" =~ [abcde]* ]]; then
    echo >&2 "Unexpected option, expected option be made of [${!options[@]}]"
    return 1
  fi
  case "$fruits" in
  -) toast+=(${options[@]}) ;;
  *a*) toast+=("${options[a]}") ;;&
  *b*) toast+=("${options[b]}") ;;&
  *c*) toast+=("${options[c]}") ;;&
  *d*) toast+=("${options[d]}") ;;&
  *e*) toast+=("${options[e]}") ;;
  esac
  if [ "${#toast[@]}" -ne 0 ]; then
    echo "Fruits chosen: ${toast[@]}"
  else
    echo "No fruits to eat!!!"
  fi
}

function case_wfallt_td() {
  # Bash added another operator
  # in the case statement such that
  # when a match is made on some nth
  # pattern of a total of m patterns,
  # the rest from n->m will be matched.
  # Stops on ;; or end of case statement
  # Perfect fall through from point of match
  local -i counter=1 input
  read -p "Add from[1-7]: " input
  if [[ ! "$input" =~ [0-7] ]]; then
    echo >&2 "Expected integer between 1-7 inclusively."
    return 1
  fi
  case "$input" in
  7) ((counter *= 2)) ;&
  6) ((counter *= 2)) ;&
  5) ((counter *= 2)) ;&
  4) ((counter *= 2)) ;&
  3) ((counter *= 2)) ;&
  2) ((counter *= 2)) ;&
  1) ((counter *= 2)) ;;
  esac
  echo "End Value: $counter"
}

# simple_case
# case_wfallt_iff
# case_wfallt_td