#!/usr/bin/env bash

# Chaining comands in bash
# 1. Piping commands
# 2. Logical chaining
# 3. Sequencial/serial chaining

function piping_commands() {
  # You can connect the output of one command as
  # input to another. Example.
  # List all directories in HOME directory
  # and highlight the lines/paths with a 'D' in them.
  ls -1 "$HOME" | grep --color=always D
  # If ls fails, it will write to stderr which the above
  # will not pass to grep. To pass, use |&
  ls -1 "/path/does/not/exist" |& grep --color=always d
  # This should highlight all lowercase d's in the error
  # returned by 'ls' command.
}

function logical_chaining() {
  # Running commands depending on the success of another
  # can be achieved by using logical operators && and ||.
  # The represent 'and' and 'or' as used in python.
  # && will run the seccond command if the first exits
  # successfully while of will run the second only if the
  # fisrt fails.
  [ -e "/path/does/not/exist" ] || echo 'Path was not found.'
  [ -e "$HOME" ] && echo 'Path was found.'
  # You can nest whole blocks using curly braces
  function test_is_file() {
    [ -f "$1" ] && {
      echo "Congratulations."
      echo "You passed a file."
    } || {
      echo "Expected a file."
      echo "Please pass a file instead"
    }
  }
  test_is_file "$HOME/Desktop"
  test_is_file "$HOME/.bashrc"
}

function serial_chaining() {
  # This is simply a list of commands
  # chained together separated by a semicolon.
  echo One; echo Two; echo Three;
  # They often have nothing/no type of interaction
  # very useful in the terminal, running multiple
  # commands in one line.
}

# piping_commands
# logical_chaining
# serial_chaining
