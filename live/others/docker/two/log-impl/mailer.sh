#!/usr/bin/env sh
printf "Logging Mailer has started.\n"
while true; do
  MESSAGE="$(nc -l -p 33333)"
  printf "[Message]: %s\n" "$MESSAGE" >"$1"
  sleep 1
done
