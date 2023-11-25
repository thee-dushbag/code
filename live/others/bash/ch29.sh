#!/usr/bin/env bash

# Bash Programmable completions.

function _mycompletion() {
  local command_name="$1" current_word="$2" previous_word="$3"
  # COMPREPLY is an array which has to be filled with possible completions
  # compgen is used to filter matching completions
  COMPREPLY=($(compgen -W 'helloworld' -- "$current_word"))
}

function _activate_comp() {
  local command_name="$1" current_word="$2" previous_word="$3"
  COMPREPLY=($(compgen -W "$(ls "$CONTENT_VENVS")" -- "$current_word" ))
}

function _activate_impl() {
  local venv="$CONTENT_VENVS/$1/bin/activate"
  if [ ! -e "$venv" ]; then
    echo >&2 "Venv not found: $1"
    return 2
  fi
  source "$venv"
}

function mycomp() {
  echo "Args: $*"
}

function _nuance_tune_opts() {
  local curr_arg prev_arg
  curr_arg=${COMP_WORDS[COMP_CWORD]}
  prev_arg=${COMP_WORDS[COMP_CWORD - 1]}
  case "$prev_arg" in
    -config)
      COMPREPLY=($(/bin/ls -1 /))
      return 0
    ;;
  esac
  echo -e "\nCurrArg: '$curr_arg' | PrevArg: '$prev_arg' | Size: $((COMP_CWORD - 1))"
  COMPREPLY=($(compgen -W '-analyze -experiment -generate_groups
  -compute_thresh -config -output -help -usage -force -lang -grammar_overrides
  -begin_date -end_date -group -dataset -nultiparses -dump_records -no_index
  -confidencelevel -nrecs -dry_run -rec_scripts_only -save_temp -full_trc
  -single_session -verbose -ep -unsupervised -write_manifest -remap -noreparse
  -upload -reference -target -use_only_matching -histogram -stepsize' -- $curr_arg))
}


function nuance_tune() {
  echo "NuanceTune Args: $*"
}


alias actcomp=_activate_impl
complete -F _mycompletion mycomp
complete -F _activate_comp actcomp
complete -o filenames -F _nuance_tune_opts nuance_tune