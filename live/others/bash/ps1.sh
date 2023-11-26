function gitPS1() {
  if git branch &>/dev/null; then
    local gitbranch="$(git branch | grep \*)"
    echo "[ ${gitbranch/\* /} ]"
  fi
}

function timePS1() {
  local time="$(date +%r)"
  echo "[ ${time} ]"
}

function headPS1() {
  echo "[ \j ][ \W ]\n\$ "
}

function venvPS1() {
  if [ -n "$VIRTUAL_ENV" ]; then
    echo "[ $(basename "$VIRTUAL_ENV") ]"
  fi
}

function lastESPS1() {
  if [ $? -eq 0 ]; then
    echo "[ Y ]"
  else
    echo "[ X ]"
  fi
}

function venvStatus() {
  if [ -n "$VIRTUAL_ENV" ]; then
    MY_VENV="$(basename "$VIRTUAL_ENV")"
  else
    unset MY_VENV
  fi
}

function gitBranchStatus() {
  if git branch &>/dev/null; then
    local gitbranch="$(git branch | grep \*)"
    MY_BRANCH="${gitbranch/\* /}"
  else
    unset MY_BRANCH
  fi
}

function commitsCountStatus() {
  if git status &>/dev/null; then
    MY_COMMITS="$(git log --oneline | wc -l)"
  else
    unset MY_COMMITS
  fi
}

function lastCmdStatus() {
  MY_LASTSTAT_CODE="$?"
  if [ $MY_LASTSTAT_CODE -eq 0 ]; then
    MY_LASTSTAT_CLR=$'\e[92;1m'
    MY_LASTSTAT=$'✓'
    unset MY_ERROR_CODE
  else
    MY_LASTSTAT_CLR=$'\e[91;1m'
    MY_LASTSTAT=$'×'
    MY_ERROR_CODE="$MY_LASTSTAT_CODE"
  fi
}

function prompt_command() {
  lastCmdStatus
  gitBranchStatus
  commitsCountStatus
  venvStatus
}

PROMPT_COMMAND=prompt_command
# export PS1="\$(lastESPS1)\$(venvPS1)\$(gitPS1)\$(timePS1)$(headPS1)"
PS1=$'\[$MY_LASTSTAT_CLR\]$MY_LASTSTAT\[\e[0m\]'
# PS1+=$' \[\e[97;1m\]\#' # Turn on command counters
PS1+=$'\[\e[91;1m\]${MY_ERROR_CODE:+ $MY_ERROR_CODE}\[\e[0m\]'
PS1+=$'\[\e[97m\]${MY_VENV:+ ($MY_VENV)}\[\e[0m\]'
PS1+=$'\[\e[97;1m\]${MY_BRANCH:+ (}\[\e[96m\]${MY_BRANCH}\[\e[97;1m\]${MY_BRANCH:+:}\[\e[96m\]${MY_COMMITS}\[\e[97;1m\]${MY_BRANCH:+)}\[\e[0m\]'
PS1+=$' \[\e[97;1m\]\W \[\e[94;1m\]\$ \[\e[0m\]'
export PS1