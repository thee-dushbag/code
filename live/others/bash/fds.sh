# Creating file descriptors

# fds directory holds my custom standard streams

# Creating a descriptor for input: descriptor number 50
exec 50<"$(realpath fds/in)"

# Creating a descriptor for output: descriptor number 51 and 52
exec 51>"$(realpath fds/out)"
exec 51>"$(realpath fds/ers)"

# Redirecting to open descriptos
echo This is for Standard Output >&51
echo This is an Error >&52
# Assuming there are some lines in fds/in
read name <&50
echo Read from stdin: $name

# Closing descriptors: 50, 51, 52
# Note the <> chars in the expressions
# <  : for input
# >  : for output
# &- : indicates closing the descriptor
exec 50<&- 52>&- 52&-

# We have also learned of grep and its amazing capapilities.
# Use man for a refresh: man grep