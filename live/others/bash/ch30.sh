#!/usr/bin/env bash

function braceExpansion() {
  # Rename file
  file="nonexistingfile.txt"
  filestem="${file%.*}" # nonexistingfile
  filesuffix="${file##*.}" # txt
  newsuffix="bak"
  touch "$file"
  newfile="$filestem.$newsuffix" # nonexistingfile.bak
  mv "$filestem."{"$filesuffix","$newsuffix"} # nonexistingfile.txt -> nonexistingfile.bak
  rm "$newfile"
}

function braceExpansionCI() {
  echo Expand from 1 to 10: {1..10}
  echo Expand from 1 to 10 padded 0\'s: {01..10}
  echo Expand from 1 to 10 padded 0\'s: {001..10}
  echo Expand from 10 to 1: {10..1}
  echo Expand from 10 to 1 padded 0\'s: {10..01}
  echo Expand from 10 to 1 padded 0\'s: {10..001}
  mkdir -p year_directories/20{22..23}_{01..12}
  rm -rfv year_directories
  echo Increments count 1-10-2: {00..10..2}
  echo s.letters: {a..z}
  echo c.letters: {A..Z}
  echo s.letters: {z..a}
  echo c.letters: {Z..A}
  echo s.letters incr 4: {a..z..4}
  echo c.letters incr 4: {A..Z..4}
  echo s.letters incr 4: {z..a..4}
  echo c.letters incr 4: {Z..A..4}
  mkdir -p root_directory_here/dir{01..5}/{simon,nganga,njoroge}
  rm -rfv root_directory_here
} 

braceExpansionCI