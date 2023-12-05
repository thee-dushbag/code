#!/usr/bin/env bash

# Read a file (data stream variable) line-by-line (and/or field-by-field)

function loop_file_line_by_line() {
  local file="text.txt" number letter
  while IFS= read -r line || [ -n "$line" ]; do
    echo "$line"
  done <"$file"
  local data='one
two
three
four
five'
  # Read from a here string
  while read number; do
    echo "No: $number"
  done <<<"$data"
  # Read from a here document
  while read number; do
    echo "Number: $number"
  done <<-EOF
  1
  2
  3
  4
  5
EOF
  # Read from a delimetered data from a pipe
  echo "A:B:C:D:E:F" | while read -d: letter; do
    echo "Letter: $letter"
  done
  # Also from a process substitution delimetered newlines
  while read letter; do
    echo "OtherLetter: $letter"
  done < <(echo $'G\nH\nI\nJ\nK\nL')

}

function loop_file_field_by_field() {
  local name file="data.txt"
  readarray -t values <"$file"
  local -i age
  while IFS=$':\n' read -r name age; do
    echo "Hello $name, you are $age years old."
  done <"$file"
  echo -e "VALUES: ${values[@]}\n"

  file="/etc/passwd"
  while IFS=: read -r username password userid groupid comment homedir cmdshell; do
    echo "$username, $userid, $homedir"
  done <"$file"
}

# loop_file_line_by_line
# loop_file_field_by_field
