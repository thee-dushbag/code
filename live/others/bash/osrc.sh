# Simply for testing testing BASH_SOURCE
# from script ch36.sh

function func_five() {
  echo "Five: ${FUNCNAME[@]}"
  echo "  BASH_SOURCE: ${BASH_SOURCE[@]}"
}