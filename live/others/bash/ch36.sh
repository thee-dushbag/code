#!/usr/bin/env bash

# Bash Internal Variables

function bash_variables() {
  # $*             -> "$1 $2 $3 $4 $5"
  # $@             -> "$1" "$2" "$3" "$4" "$5"
  # $#             -> number of arguments to the script/function
  # $?             -> exit status of the last command
  # $!             -> pid of the last job run in the background
  # ${n}           -> nth positional argument, also written as $n for 0-9
  # $0             -> name of the script running
  # $IFS           -> internal field separator. default is newline (\n), tab (\t) and space ( )
  # $PATH          -> paths where executables can be found
  # $OLDPWD        -> Previous working directory
  # $PWD           -> Present working directory
  # $FUNCNAME      -> Array of function names in the execution stack.
  # $BASH_SOURCE   -> Array containing source paths for elements in FUNCNAME array.
  # $BASH_ALIASES  -> Associative array containing all currently defined aliases
  # $BASH_REMATCH  -> Array of matches from the last regex match
  # $BASH_VERSION  -> Bash version string
  # $BASH_VERSINFO -> An array of 6 elements with bash version information
  # $BASH          -> Absolute path to currently execution bash shell itself
  # $BASH_SUBSHELL -> Bash subshell level
  # $UID           -> Real user ID of process running bash
  # $PS1           -> Primary command line input.
  # $PS2           -> Secondary command line input.
  # $PS3           -> Tertiary command line input.
  # $PS4           -> Quaternary command line input.
  # $RANDOM        -> A pseudo random integer between 0 to 32767
  # $REPLY         -> Variable used by read ans select for its user collected input
  # $PIPESTATUS    -> Array variable that holds the exit status values of each command
  #                   in the most recently executed foreground pipeline
  # $HISTSIZE      -> maximum number of remembered commands
  # $HOME          -> Home directory of the user
  # $$             -> pid of the current process
  # $BASHPID       -> pid of the current instance of bash
  # $BASH_ENV      -> an env variable pointing to bash statup file to be read when a script is invoked
  # $EDITOR        -> default editor to be used by programs and scripts, usually vi or emacs
  # $HOSTMANE      -> hostname assigned to the system during startup
  # $HOSTTYPE      -> identifies the hardware
  # $MACHTYPE      -> includes info about os and hardware
  # $OSTYPE        -> return info about os running on machine
  # Arguments are separated by IFS which doesn't have to be a space
  :
}

function func_four() {
  echo "Four: ${FUNCNAME[@]}"
  echo "  BASH_SOURCE: ${BASH_SOURCE[@]}"
  . osrc.sh
  func_five
}
function func_three() {
  echo "Three: ${FUNCNAME[@]}"
  echo "  BASH_SOURCE: ${BASH_SOURCE[@]}"
  func_four
}
function func_two() {
  echo "Two: ${FUNCNAME[@]}"
  echo "  BASH_SOURCE: ${BASH_SOURCE[@]}"
  func_three
}
function func_one() {
  echo "One: ${FUNCNAME[@]}"
  echo "  BASH_SOURCE: ${BASH_SOURCE[@]}"
  func_two
}

function seefuncs() {
  echo "SeeFuncs: ${FUNCNAME[@]}"
  echo "  BASH_SOURCE: ${BASH_SOURCE[@]}"
  func_one
}

seefuncs

# bash_arguments "$@"
