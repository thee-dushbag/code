#! /usr/bin/env bash

function _cleanup() {
  rm -rfv files
}

function _prepare() {
  mkdir files
  touch files/file_{one,two}.txt
  ln files/file_{one,three}.txt
  ln -s files/file_{two,four}.txt
  touch readable executable writable
  chmod ugo= readable executable writable
  chmod u+r readable
  chmod u+w writable
  chmod u+e executable
  _addcontents
}

function _addcontents() {
  cat >files/file_one.txt <<EOF
Hello World
My name is Simon
I have a sister.
I live in Nairobi
I am Kenyan
EOF
  cat >files/file_two.txt <<EOF
Hello World
My name is Faith
I have a brother.
I live in Nairobi
I am Kenyan
EOF
}

function heredoc() {
  # The EOF bit of string you see,
  # can be named to anything. It is
  # called the limitstring
  local name=Simon\ Nganga
  sudo -s <<-'EOF'
    name=Mark\ Njoroge
    ls -A /root
    echo My name is ${name:-Anonymous}
EOF
  # The symbol <<- is different from <<
  # as it signifies that the content before
  # the limitstring will be tabbed and the tabs
  # can be removed on processing.
  cat <<'LimitString'
We have used another limitstring
We named it 'LimitString'
    This is a tabbed line on <<
LimitString
  cat <<-EOF
    This is a tabbed line on <<-
EOF
}

function herestr() {
  while read -d ' ' fruit; do
    echo Fruit: \'${fruit^}\'
  done <<<"orange apple pineapple avocado "
}

function cdtest() {
  declare sep=','
  local file="$1"
  if [ ! -e "$file" ]; then
    echo >&2 "Path Not Found$sep$file"
  fi
  if [ -d "$file" ]; then
    echo "Directory$sep$file"
  fi
  if [ -f "$file" ]; then
    echo "Regular File$sep$file"
  fi
  if [ -p "$file" ]; then
    echo "Named Pipe$sep$file"
  fi
  if [ -S "$file" ]; then
    echo "Socket$sep$file"
  fi
  if [ -b "$file" ]; then
    echo "Block Device$sep$file"
  fi
  if [ -L "$file" ]; then
    echo "Symbolic Link$sep$file"
  fi
  if [ -c "$file" ]; then
    echo "Character Device$sep$file"
  fi
}

function strop() {
  # String comparisson.
  local word='Hello World'
  local pattern='H???? *'
  if [[ "$word" == $pattern ]]; then
    echo "Match Found: '$word' matches the pattern /$pattern/"
  else
    echo "Match Fail: '$word' does not match pattern /$pattern/"
  fi
  # You can also use != to check if a string does not match to a pattern
  # The operators < and > are used to match string lexicographically

  # -n flag to check if string is Non-Empty
  local string=Not\ Empty
  if [ -n "$string" ]; then
    echo "The string is Non-Empty: '$string'"
  else
    echo "The string is Empty."
  fi
  # -z flag to check if string is empty or contains only spaces
  if [ -z "$string" ]; then
    echo "String is Empty or contains spaces."
  else
    echo "String is Non-Empty: '$string'"
  fi
}

function fileop() {
  if [ "files/file_one.txt" -ef "files/file_three.txt" ]; then
    echo These are the same exact files in memory.
  else
    echo Files are different in memory.
  fi
  if [ "files/file_two.txt" -ef "files/file_four.txt" ]; then
    echo These are the same exact files in memory.
  else
    echo Files are different in memory.
  fi
  if [ "files/file_one.txt" -ef "files/file_two.txt" ]; then
    echo These are the same exact files in memory.
  else
    echo Files are different in memory.
  fi

  if cmp -s -- "files/file_one.txt" "files/file_three.txt"; then
    echo \[CMP\]: These are the same exact files in memory.
  else
    echo \[CMP\]: Files are different in memory.
  fi
  if cmp -s -- "files/file_two.txt" "files/file_four.txt"; then
    echo \[CMP\]: These are the same exact files in memory.
  else
    echo \[CMP\]: Files are different in memory.
  fi
  if cmp -s -- "files/file_one.txt" "files/file_two.txt"; then
    echo \[CMP\]: These are the same exact files in memory.
  else
    echo \[CMP\]: Files are different in memory.
  fi

  if diff -u "files/file_one.txt" "files/file_three.txt"; then
    echo \[DIFF\]: These are the same exact files in memory.
  else
    echo \[DIFF\]: Files are different in memory.
  fi
  if diff -u "files/file_two.txt" "files/file_four.txt"; then
    echo \[DIFF\]: These are the same exact files in memory.
  else
    echo \[DIFF\]: Files are different in memory.
  fi
  if diff -u "files/file_one.txt" "files/file_two.txt"; then
    echo \[DIFF\]: These are the same exact files in memory.
  else
    echo \[DIFF\]: Files are different in memory.
  fi
}

function _fattr_impl() {
  local file="$1"
  echo -n "$file: "
  if [ -r "$file" ]; then
    echo -n readable
  else
    echo -n not-readable
  fi
  echo -n \ 
  if [ -w "$file" ]; then
    echo -n writable
  else
    echo -n not-writable
  fi
  echo -n \ 
  if [ -x "$file" ]; then
    echo -n executable
  else
    echo -n not-executable
  fi
  echo
}

function fattr() {
  local files=(readable writable executable)
  for file in "${files[@]/#/files\/}"; do
    _fattr_impl "$file"
  done
}

function numop() {
  # Numerical comparissons use
  # -eq, -gt, -ge, -lt, -le, -ne
  declare -i age=12
  if [ $age -ge 18 ];then
    echo You can VOTE\!\!\!
  else
    echo You are not allowed to VOTE\!\!\!
  fi
  # Note: < and > are reserved for
  # string lexicographical comparisson.
  if [ 9 < 10 ]; then
    echo Error: 9 \< 10
  else
    echo Okay : 9 \> 10
  fi
}

