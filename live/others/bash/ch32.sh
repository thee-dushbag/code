#!/usr/bin/env bash

function pingnmap() {
  local ip port nmap_yes=0 ping_yes=0
  while getopts ':nti:p:v' opt; do
    case "$opt" in
    i)
      ip="$OPTARG"
      ;;
    p)
      port="$OPTARG"
      ;;
    n)
      nmap_yes=1
      ;;
    t)
      ping_yes=1
      ;;
    v)
      echo "pingnmap version: 1.0.0"
      ;;
    *)
      echo >&2 "Invalid option '$opt'"
      echo "Usage: pingnmap -[n|t[i|p]|v]"
      ;;
    esac
  done

  if [ "$nmap_yes" -eq 1 ] && [ ! -z "$ip" ] && [ ! -z "$port" ]; then
    nmap -p "$port" "$ip"
  fi
  if [ "$ping_yes" -eq 1 ] && [ ! -z "$ip" ]; then
    ping -c 5 "$ip"
  fi

  shift $((OPTIND - 1))
  if [ ! -z "$@" ]; then
    echo >&2 "Bogus arguments at the end: $@"
  fi
}

# pingnmap "$@"

# Debugging.
# ----------
# 1) Use -n flag to check for syntax error.
#    Example: bash -n sourcefile.sh
# 2) Enable bash debugger using -x
#    Two ways to enable it:
#    a) bash -x script.sh
#       OR
#       bash --debug script.sh
#    b) set -x
#       bash script.sh
#    To disable it, run `set +x`
