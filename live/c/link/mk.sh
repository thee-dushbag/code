build() {
  for name; do
    $CC -o "$name" "$name$EXT" -L"$(realpath ./lib)" -l"$name" -I"$(realpath ./include)" -Wl,-rpath,"$(realpath ./lib)"
  done
}

EXT=.cpp CC=g++ build os
EXT=.c CC=gcc build app

