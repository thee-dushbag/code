#!/usr/bin/env sh

_send_email() {
  sender="$1"
  receiver="$2"
  subject="$3"
  body="$4"
  exec 100>/dev/tcp/192.168.0.100/8080
  echo -e "POST /$sender/$receiver HTTP/1.1\r\nSubject: $subject\r\nConnection: close\r\nBody: $body\r\n\r\n" >&100
  exec >&100-
}

printf "Live MAiler has started."
while true; do
  MESSAGE="$(nc -l -p 33333)"
  _send_email "$1" "$2" "App Status" "$MESSAGE"
  sleep 1
done
