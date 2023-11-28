#\!/usr/bin/env bash

awk -F: '{print $2}' cmds.txt
