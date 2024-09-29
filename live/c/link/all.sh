#!/usr/bin/env bash

./mklib.sh
./link.sh os arch
./link.sh app uber
./mk.sh

