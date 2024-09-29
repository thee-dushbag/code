mklib () { 
    for lib; do
        $CC -shared -fPIC -Iinclude -o "lib/lib$lib.so" "src/$lib$EXT";
    done
}


CC=g++ EXT=.cpp mklib debian ubuntu arch manjaro
CC=gcc EXT=.c mklib google uber

