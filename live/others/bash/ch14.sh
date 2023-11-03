#!/usr/bin/env bash
# Learning bash Function and parameter expansion

function str.upper() {
  echo "${*^^}"
  # declare -u ustr="$*"
  # echo "$ustr"
}

function str.lower() {
  echo "${*,,}"
  # declare -l lstr="$*"
  # echo "$lstr"
}

function _title_word_impl() {
  local word="${*,,}"
  echo "${word^}"
}

function str.cap() {
  echo "$(_title_word_impl "$@")"
}

function str.title() {
  local words
  IFS=' '
  for sentence; do
    words=()
    for word in $sentence; do
      words+=($(_title_word_impl "$word"))
    done
    echo "${words[*]}"
  done
}

# To set a default value to a variable if one was not passed
# use: echo ${name:-anonymous}

function _greet_impl() {
  echo "Hello $(str.title "${1:-anonymous}"), how was your day?"
}

function greet() {
  for name; do
    _greet_impl "$name"
  done
}

function getfunc() {
  declare -f "$@"
}

# Functions that support named parameters can be achieved by
# using the case...esac control structure to retrieve the values.
# Example

function namedparam() {
  . ./ch10.sh
  opts "$@"
}

# Bash Parameter Expansion
function capparam() {
  # Modyfying Case of alphabetic chars.
  local var="simon nganga"
  echo Original Value: ${var}
  echo First Character Uppercase: ${var^}
  echo All Character Uppercase: ${var^^}
  # This can also be acieved using declare -u ustr="$var"
  var=${var^^}
  echo -e \\nOriginal Value: ${var}
  echo First Character Lowercase: ${var,}
  echo All Character Lowercase: ${var,,}
  # This can also be achieved using declare -l lstr="$var"
  var=SiMoN\ nGaNgA
  echo -e "\nOriginal Value: ${var}"
  # My Linter Is Giving errors on the next two lines, but they Run Completly Fine.
  echo "Toggle First Character: ${var~ }"
  echo "Toggle All Characters: ${var~~}"
  echo "Length Of Parameter: ${#var}"
}

function strre() {
  local var=Simon\ Nganga\ Njoroge
  echo Original Value: $var
  echo First Match[N -\> n]: ${var/N/n}
  echo All Matches[N -\> n]: ${var//N/n}
  echo Match at Beginning[Sim -\> sIM]: ${var/#Sim/sIM}
  echo Match at End[oge -\> OGE]: ${var/%oge/OGE}
  echo Delete a pattern: ${var/joroge/}
  local names=("${var/ / }")
  echo Size: Name: ${#var}, Names: ${#names[@]}
  echo Add Prefix to Array Items[NAME -\> Name_NAME]: ${names[@]/#/Name_}
  echo Add Suffix to Array Items[NAME -\> NAME.Name]: ${names[@]/%/.Name}
}

function substr() {
  local var=Simon\ Nganga\ Njoroge
  # General Syntax Of Substring: '${var:<offset>:<length>}'
  echo Original Name: $var
  echo First Name: ${var:0:5}
  echo Middle Name: ${var:6:6}
  # Need to add a space between : and - in -7 to prevent confusion
  # with default value variable like ${var:-7} which would return 7
  # if var is undefined variable. Alternatively you can use parenthesis
  # echo Last Name: ${var:(-7)}
  echo Last Name: ${var: -7}
  # echo Middle Name: ${var:(-14):(-7)}
  # echo Middle Name: ${var:(-14):6}
  # Negative numbers means start counting from the end.
  local names=($var)
  echo Second Last Eleemnt: ${names[@]:(-2):1}
  echo Last Eleemnt: ${names[@]:(-1)}
  # Delete patters from the start and end of strings.
  echo Delete first five chars: ${var#?????}
  echo Delete to the first space: ${var#* }
  echo Delete to the last space: ${var##* }
  echo Delete last seven chars: ${var%???????}
  echo Delete to the last space: ${var% *}
  echo Delete from the first space: ${var%% *}
}

function pind() {
  # You can store the name of a variable in another variable
  # and indirectly get the value of the first variable from the second
  # variable. This is called variable indirection.
  local msg="This is a Secret Message."
  local var=msg
  echo Value stored in var: $var
  echo Value of variable stored in var: ${!var}
}

function dvsub() {
  # Default value substitution occurs if
  # the variable is unset or null.
  echo Value: ${var:-VAR_IS_UNSET}
  echo ValueAfter: $var
  local var=
  echo Value: ${var:-VAR_IS_EMPTY}
  echo ValueAfter: $var
  var=ValueFromVar
  echo Value: ${var:-VAR_HAS_VALUE}
  echo ValueAfter: $var

  # Setting on Check
  # To be able to assign on check for existence
  unset var
  echo
  echo Value: ${var:=VAR_IS_UNSET}
  echo ValueAfter: $var
  local var=
  echo Value: ${var:=VAR_IS_EMPTY}
  echo ValueAfter: $var
  var=ValueFromVar
  echo Value: ${var:=VAR_HAS_VALUE}
  echo ValueAfter: $var

  # While :- returns the default if the variable
  # is unset or empty, - returns the default only
  # if the variable is unset
  unset var
  echo
  echo Value: ${var-VAR_IS_UNSET}
  local var=
  echo Value: ${var-VAR_IS_EMPTY}
  var=ValueFromVar
  echo Value: ${var-VAR_HAS_VALUE}

  # Similar to above. := assigns the default if
  # the variable is unset or empty, = only sets
  # if the variable was unset
  unset var
  echo
  echo Value: ${var=VAR_IS_UNSET}
  local var=
  echo Value: ${var=VAR_IS_EMPTY}
  var=ValueFromVar
  echo Value: ${var=VAR_HAS_VALUE}

  # Using :+ you can use a given value as an
  # alternative to an existing variable if it
  # is empty or has a value
  unset var
  echo
  echo Value: ${var:+VAR_IS_UNSET}
  local var=
  echo Value: ${var:+VAR_IS_EMPTY}
  var=ValueForVar
  echo Value: ${var:+VAR_HAS_VALUE}
  # Omitting the :, we get an alternative only
  # if the variable was set to a non-empty value
  unset var
  echo
  echo Value: ${var+VAR_IS_UNSET}
  local var=
  echo Value: ${var+VAR_IS_EMPTY}
  var=ValueForVar
  echo Value: ${var+VAR_HAS_VALUE}

  # Errors on using unset or empty variables can
  # be achieved using the operator :? using the syntax
  # ${VariableName:?Error Message Here}
  # Uncomment to test this feature.
  unset var
  echo
  # echo Value: ${var:?VAR_IS_UNSET}
  local var=
  # echo Value: ${var:?VAR_IS_EMPTY}
  var=ValueForVar
  echo Value: ${var:?VAR_HAS_VALUE}
  # As Usual, omitting the comma gives way for a new
  # operator ? which raises an error only if the variable
  # is unset. Uncomment to test this feature.
  unset var
  echo
  # echo Value: ${var?VAR_IS_UNSET}
  local var=
  echo Value: ${var?VAR_IS_EMPTY}
  var=ValueForVar
  echo Value: ${var?VAR_HAS_VALUE}
}
