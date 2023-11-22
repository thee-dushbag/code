# Creating file descriptors
# fds directory holds my custom standard streams

# Closing descriptors: 50, 51, 52
# Note the <> chars in the expressions
# <  : for input
# >  : for output
# &- : indicates closing the descriptor

# We have also learned of grep and its amazing capapilities.
# Use man for a refresh: man grep

# Operations with file descriptors.
# 1. Openning file descriptors
# 2. Closing file descriptors
# 3. Move file descriptors
# 4. Duplicatiing descriptors
# 5. Appending standard output/error

fdsdir="$(realpath "./fds")"

function openning_and_closing_fds() {
  # Openning file descriptors for:
  # 1. input
  exec 50<"$fdsdir/in"
  # 2. output/error
  exec 51>"$fdsdir/out" 52<"$fdsdir/err"

  # Using fds for input and output
  read name <&50
  echo "Hello $name, how was your day?" >&51

  # Closing fds from:
  # 1. input
  exec 50<&-
  # 2. output/error
  exec 51>&- 52>&-
}

function moving_fds() {
  # Open fd for testing
  exec 50<"$fdsdir/in"
  # Move the old fd 50 to new fd 60
  read old_name <&50
  echo "Old Name: $old_name"
  exec 60<&50- # Note: 50 will be closed
  read new_name <&60
  echo "New Name: $new_name"
  # Close the test fd
  exec 60<&-
}

function duplicating_fds() {
  # Open fd for testing
  exec 50<"$fdsdir/in"
  # Move the old fd 50 to new fd 60
  read old_name <&50
  echo "Old Name: $old_name"
  exec 60<&50
  read new_name <&60
  echo "New Name: $new_name"
  # Close the test fd
  exec 60<&- 50<&- # Note, 50 is still open
}

function appending_to_output_fds() {
  # Open fd for testing
  exec 50>>"$fdsdir/out" # Openning without truncating the source
  echo Hello World >&50
  echo My name is Simon >&50
  echo I have a sister called Mary >&50
  echo "(*o*) Hoot Hooot" >&50
  # Close the test fd
  exec 50>&-
}