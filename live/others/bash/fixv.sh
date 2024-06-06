#!/usr/bin/env bash

# this is a very dangerous script, wouldn't wanna execute it by accident
echo >&2 Make sure you wanna do this man
exit 1

venvs=($CONTENT_VENVS/*)

for venv in "${venvs[@]}"; do
	echo VENV: $venv
	if [ -d $venv ] && [ ! -L "$venv" ]; then
		# $venv is an actual virtual env directory
		target_venv_name="$(basename "$venv")"
		symbolic_venv_name="${target_venv_name}2"
		files=($(grep --exclude-dir=__pycache__ -Ilr "$symbolic_venv_name" "$venv"))
		for file in "${files[@]}"; do
			sed -i "s/$symbolic_venv_name/$target_venv_name/g" "$file"
		done
	else
		# $venv is a symbolic link from $symbolic_venv_name to $target_venv_name
		rm "$venv" # symbolic link to the actual virtual env
	fi
done
