#!/usr/bin/env bash

# Bash Background Jobs

function create_sleep_jobs() {
  sleep 10 &
  sleep 20 &
  sleep 30 &
  # ^- create 3 sleep jobs
  jobs -l # <- List the jobs
  # Options:
  # 1) -l  List the jobs as normal but also include thir pids
  # 2) -s  List only Stopped jobs
  # 2) -r  List only Running jobs
  # 2) -p  List the Running jobs pids
  # Output:
  # [1]   Running                 sleep 10 & (wd: ~)
  # [2]-  Running                 sleep 20 & (wd: ~)
  # [3]+  Running                 sleep 30 & (wd: ~)

  # Filed |  Sample     | Purpose
  # 1     |  [1], [2]   | Job Ids
  # 2     |  8173       | Job PID (Use the -l flag to show this)
  # 3     |  +/-        | Denote the default/next job, used by fg/bg
  # 4     |  Running    | State of the job, others: Done, Terminated and Stopped
  # 5     |  sleep 10 & | The task run in the background
  # 6     | (wd: ~)     | The directory in which the job was started
}

function start_jobs_if_none() {
  if [ -z "$(jobs -p)" ]; then
    create_sleep_jobs
  fi
}

function bring_foreground() {
  start_jobs_if_none
  echo Press Ctrl+z to stop the job.
  fg # <- Brings a job to the foregound
  # Simply send SIGCONT to the process using its pid
  # Alternatively but will remain in the background...
  # kill -s SIGSTOP %{jobid}
  # Syntax: fg %{jobid}
  #   Without an argument, it brings the last added job
  # Syntax: fg %?{reg}
  #   Returns the job whose command had a substring reg,
  #   if multiple jobs satisfy this, it will produce an error
}

function move_background() {
  start_jobs_if_none
  bg # <- Run a stopped job in the background
  # If no argument is provided, the job with option + will be used
  # It's like
  # kill -s SIGCONT %{jobid}
  # You can also run a job in the background immediately
  # by appending an ampersand at the end of the command, eg
  # sleep 40 &
  # For an already running process in the foreground, it can
  # be stopped by sending SIGSTOP by pressing Ctrl+z
}

function must_be_interactive() {
  case "$-" in
  *i*)
    echo >&2 Running interactively...
    ;;
  *)
    echo >&2 Source this script to interact with the jobs...
    return 2
    ;;
  esac
  create_sleep_jobs
  bring_foreground
  move_background
}

must_be_interactive
