#!/usr/bin/env bash

# Process substitution.
# ---------------------
# Unlike sub-shells, they do not run
# in their own contexts. Therefore
# retain any variables in the scope
# they are used.

# Using the |(pipe), &(job) and ()(sub-shell)
# operators runs the respective commands in
# a sub-shell.

# Takes two forms:
#     >(command)
#     <(command)

# Process substitution returns a file,
# specifically, it is a file descriptor
# in the current process but it is basically
# a file. The process is run asyncronously.

# 1. >(command)
#   This form is used to write data to that
#   command when it reads data.

# 2. <(command)
#   This form is meant to be read from as
#   its stdout output will be transferred
#   via that returned file to the current reader.

function compare_results() {
  local url="$1"
  if [ -z "$url" ]; then
    url="https://example.com"
  fi
  # Using temporary files
  local f1="$(mktemp)" f2="$(mktemp)"
  curl "$url/page1" >"$f1" 2>/dev/null
  curl "$url/page2" >"$f2" 2>/dev/null
  diff "$f1" "$f2"
  rm "$f1" "$f2"

  # Using process substitution.
  diff <(curl "$url/page1" 2>/dev/null) <(curl "$url/page2" 2>/dev/null)
}

function feed_while_loop() {
  # Feed while loop with the output of another command
  local names=$'Simon\nFaith\nDarius\nHarisson\nLydia'
  # 1. Using here-strings
  while read name; do
    echo "Hello $name? How was your day?"
  done <<<"$names"
  echo # 2. Using process-substitution
  local file="$(mktemp)"
  echo "$names" >"$file"
  while read name; do
    echo "Hello $name? How was your day?"
  done < <(cat "$file")
  rm "$file"
}

function process_multiple_files() {
  local bigfile="$(mktemp)" otherfile="$(mktemp)"
  echo {1..100000} | tr \  \\n >"$bigfile"
  # Note: This is all done concurrently as the
  # number of lines is counted, the file is also
  # being compressed by gzip.
  tee >(wc -l >&2) <"$bigfile" | gzip >"$otherfile"
  rm "$bigfile" "$otherfile"
}

function async_proof() {
  # The tee command reads from its stdin and writes to all
  # files supplied as its arguments and also to its stdout.
  # We supply a for loop counting from 1 to 10 as a stream
  # for its input and write the output to process substitution
  # fd files returned by the showme procee substitution.
  # To prove this is asynchronous, for each read number,
  # the number is written to all output files including
  # the stdout.
  function showme() {
    local liner="$1"
    while read line; do
      echo "$liner: $line"
    done
  }
  tee >(showme "This is line" >&2) >(showme "Counter at" >&2) < <(for i in {1..10}; do
    echo $i
    sleep 0.5
  done) | showme "Outside count"
}

# Coproceses basics
function greeter_coproc() {
  function hello() {
    while read name; do
      if [[ "$name" == "--stop--" ]]; then # Special token to signify CLOSE operation
        break
      fi
      echo "Hello $name, how are you today?"
    done
  }
  # Create a coprocess with accessible fds
  # in the variable GREETER in the form
  # [outputfd, inputfd] array
  coproc GREETER { hello; }
  local names=(Simon Nganga Njoroge)
  for name in "${names[@]}"; do
    echo Input: $name # Show the input going in.
    echo $name >&${GREETER[1]} # pass a name to the coprocess
    read result <&${GREETER[0]} # read the result from the coprocess
    echo Output: $result # show the output coming out.
  done
  # Stop the coprocess using our 
  echo --stop-- >&${GREETER[1]} # Send our custom stop signal to the coprocess
}