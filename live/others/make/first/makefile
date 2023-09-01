WDIR=`pwd`

CC=g++-12 -std=c2x -Wall -w -g

INCLUDE_DIR=${WDIR}/include
LIBRARY_DIR=${WDIR}/lib
VPATH=./lib

.PHONY=all run

FLAGS=-L${LIBRARY_DIR}
CFLAGS=-I${INCLUDE_DIR} ${FLAGS}
LDFLAGS=-Wl,-rpath,${LIBRARY_DIR} ${FLAGS}

main: main.c libmymath.a(mymath.o)
libmymath.a(mymath.o): mymath.o
mymath.o: mymath.c

clean:
	rm -rfv ./main *.a *.o