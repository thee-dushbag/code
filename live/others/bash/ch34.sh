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

function regexshopt() {
  # Set options for glob can affect
  # matching for the globstar and
  # case sensitivity for regex matching
  # Shopt Options:
  # 1) failglob - Fails if no match was found
  # 2) nullglob - Returns nothing if no match was found
  # 3) nocaseglob - Ignores cases when matching
  # 4) nocesamatch - Ignores case when using =~ matching operator
  # 5) dotglob - Returns dotfiles as part of the glob result if any
  # 6) globstar - Matches all possible paths from cwd used as **
  # 7) extglob - Extends bash's builtin globbing system with
  #              ?(), *(), +(), @(), !(). The patters in the parens
  #              are separated by |
  # Note: if neither failglob nor nullglob is set when no
  #       match was found for a glob pattern, the pattern is returned.
  #       Also, failglob superceds nullglob.
  # *, **, ?, [] -> globs
  # ? -> matches exactly one character
  # * -> matches more than one character
  # ** -> mathces the whole tree with the cwd as root node
  # [] -> any character in the brace is matched exactly once.
  #       can also match character classes ad negative matches.
  #       character class [:class:], eg *[[:digit:]]*
  #       negative match [^<chars>] or [!<chars>], eg [^mc]acy
  #       ranges [a-z], [0-9] ...
  :
}

function regex2() {
  # The patterns matched by =~ are stored in the array BASH_REMATCH
  # where the 0'th index holds the whole match, and the i'th index
  # holds the i'th group
  local date=20150624
  if [[ -n "$1" ]]; then
    date="$1"
  fi
  [[ "$date" =~ ^[0-9]{8}$ ]] || return 1
  [[ "$date" =~ ^([0-9]{4})([0-9]{2})([0-9]{2})$ ]] || return 1
  declare -a months=(january february march april may june july august september october november december)
  declare -a days=(sunday monday tuesday wednesday thursday friday saturday)
  local year="${BASH_REMATCH[1]}"
  local month="${BASH_REMATCH[2]}"
  local day="${BASH_REMATCH[3]}"
  local wday="$(expr $day % ${#days[@]})"
  echo "Full Date: $date | Year: $year | Month: ${months[month]^} | Day: ${days[wday]^}"
  echo "Posix Date: $day/$month/$year"
  echo "Formatted Date: ${months[month - 1]^} $day, $year."
}

function regex3() {
  read -p Name:\  name
  local pat="^((Mr|Mrs|Miss|Sir|Madam).? )?([A-Z][a-z]+) ([A-Z][a-z]+)$"
  if [[ "$name" =~ $pat ]]; then
    echo "Prefix: ${BASH_REMATCH[2]}"
    echo "First Name: ${BASH_REMATCH[3]}"
    echo "Last Name: ${BASH_REMATCH[4]}"
    echo "Valid name: ${BASH_REMATCH[0]}"
  else
    echo "Invalid name: $name"
  fi
}
