# Array indexing in bash starts on index 0

function arrdelim() {
  local names=(Simon Nganga Njoroge Faith Njeri) counter=1
  for name in "${names[@]}"; do
    echo $counter: $name
    ((counter++))
  done
}

function warr() {
  local names=(Simon Nganga Njoroge Faith Njeri)
  echo First Name: ${names[0]}
  echo Last Element: ${names[-1]} # OR ${names[@]: -1} # Note the space
  echo All Names\(Separately\): ${names[@]}
  echo All Names\(Single String\): ${names[*]}
  echo All Elements from index 1 all quoted separately: ${names[@]:1}
  echo Elements from index 1 to 3: ${names[@]:1:3} # Inclusive
  # String Operations
  echo Substring of \'${names[0]}\'[1:4]: ${names[0]:1:4} # chars from index 1 to 4
}

function arrmod() {
  local names=(Simon Nganga Njoroge Faith Njeri)
  names+=(Lydia)
  # # OR
  # names=("${names[@]}" Lydia)
  echo Append to array: ${names[@]}
  names=(Wanjiru "${names[@]}")
  echo Insert at beginning: ${names[@]}
  names=("${names[@]:0:3}" Ruth "${names[@]:3}")
  echo Insert at any index, eg 3: ${names[@]}
  unset -v 'names[3]'
  echo Delete elements from array, eg index 3: ${names[@]}
}

function arrops() {
  local names=([2]=Simon [5]=Nganga [3]=Njoroge)
  echo Current Array: ${names[@]}
  echo Size of array: ${#names[@]}
  echo Array indicies: ${!names[@]}
  echo Array access, eg index 5: ${names[5]}
  names=("${names[@]}") # Reassigning the array after operations like delete.
  echo Reindexing the array: ${!names[@]}
  echo Iterating over an array.
  for name in "${names[@]}"; do
    echo \ \ - Name: $name
  done
  # OR, which depends on the array indicies being well sorted
  # for ((index=0; index < ${#names[@]}; index++)); do
  #   echo \[$index\]: Name: ${names[$index]}
  # done
}

function assocarr() {
  declare -A names
  names=([sis]=Faith\ Njeri [me]=Simon\ Nganga [mum]=Lydia\ Njeri)
  echo Array values: ${names[@]}
  echo Array keys: ${!names[@]}
  echo Array size: ${#names[@]}
  echo Array iteration:
  for key in "${!names[@]}"; do
    echo \ \ - [$key]: \'${names[$key]}\'
  done
  # Printing can also be achieved by.
  # declare -p names
  unset names[me]
  echo Delete an element, eg [me]: ${names[@]}
  unset names
  echo Delete an array: ${names[@]} \(Deleted\)
}

function rfiarr() {
  read -r -d \\n -a lines <text.txt
  for counter in $(seq 0 ${#lines[@]}); do
    if [ -z "${lines[$counter]}" ]; then continue; fi
    echo $(expr $counter + 1). ${lines[$counter]}
  done
}