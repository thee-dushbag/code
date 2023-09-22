#!/bin/env bash

BASE_DIR="/home/simon/Content/code/live/others/concurrency-in-python-with-asyncio-master"
TARGET=$1

if [[ "${#TARGET}" -eq 0 ]]; then
    echo Invalid chapter index >&2
    return 1
fi

export CHAPTER_IDX=$TARGET

if [[ "$TARGET" -lt 10 ]]; then
    TARGET="0$TARGET"
fi

export CHAPTER="$BASE_DIR/chapter_$TARGET"

if [[ ! -e "$CHAPTER" ]]; then
    echo "Chapter folder was not found: $CHAPTER" >&2
    return 2
fi

function _file() {
    local TARGET="$1"
    if [[ "${#TARGET}" -eq 0 ]]; then
        echo Invalid listing index: \'$TARGET\' >&2
        return 1
    fi
    local _target_file="$CHAPTER/listing_${CHAPTER_IDX}_${TARGET}.py"
    if [[ ! -e "$_target_file" ]]; then
        echo "Listing file was not found: $(realpath "$_target_file" --relative-to .)" >&2
        return 2
    fi
    echo "$_target_file"
}

function rpy() {
    local target="$1"
    local main_file="$(_file "$target")"
    if _file "$target" &>/dev/null; then
        shift
        py "$main_file" $@
    else
        echo An Error Occurred running file: \'$main_file\' >&2
        return 2
    fi
}