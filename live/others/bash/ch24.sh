# !/usr/bin/env bash

# Bash History Substitution
# echo Hello World

# List all previous commands
history
# Options:
#    -c      clear all history
#    -d n    delete entry n in history
#    -w      overwrite the history file with the current history
#    -a      append the current history to the history file
#
# $HISTFILE or ~/.bash_history is used as the history file.

# To prevent a command from being stored in history,
# prepend it with a space. Example:
# $echo Hello world        <- will be stored in history
# $ echo My password is DancingWithMe  <- this will not be stored

# Event Designators
# !n        -> expands to the n command in history
# !!        -> expands to the last command
# !text     -> expands to the last command starting with text
# !?text    -> expands to the last command containing text
# !-n       -> expands to the last nth command
# ^foo^bar  -> expands to the last command with the occurrence
#              of foo replaced with bar
# !#        -> expands to the current command

# Word Designators
# !^        -> expands to the first argument of the most recent command
# !$        -> expands to the last argument of the most recent command
# !:n       -> expands to the nth argument of the most recent command
# !:x-y     -> expands to the args x through y of the most recent command
# !*        -> expands to all arguments of the most recent command. 
#              similar to !:^-$

# Modifiers
# !:s/foo/bar    -> replace the first occurrence of foo with bar in the last command
# !:gs|foo|bar   -> replace the all occurrences of foo with bar in the last command
# !:r            -> remove the file extension from the last command
# !:h
# !:t

# Search for a command in history with a certain pattern
# press Ctrl-r and type the pattern then click Enter when
# the desired command appears, or press Ctrl-r again to
# search for the pattern upwords in the history.

# Get the Nth argument in the first chained command
# using binary op like &&. Accessor is !#:N
# Example:
#      echo one two three && mkdir !#:2 && cd !#:2 && cd .. && rmdir !#:2
# expands to:
#      echo one two three && mkdir two && cd two && cd .. && rmdir two
