[[ "${LINKDIR:=./lib}" != / ]] && LINKDIR="${LINKDIR%/}"

if [[ $# -ne 2 ]]; then
  echo >&2 "Usage: link.sh <link_name> <target_name>"
  echo >&2 "Effect: Create link '$LINKDIR/lib<link_name>.so' --> '$LINKDIR/lib<target_name>.so'"
  exit 1
fi

link="$LINKDIR/lib$1.so" target="$LINKDIR/lib$2.so"

ln -frs "$target" "$link"

