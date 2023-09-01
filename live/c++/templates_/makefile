CC=clang++ -std=c++2b -g -I. -w
CC=g++-12 -std=c++23 -I.
INCLUDE_DIR=${HOME}/Content/code/lib/include
TARGET=main
.PHONY=all clean

all: ${TARGET} exe

clean: ${TARGET}_clean

exe:
	./${TARGET}

${TARGET}: ${TARGET}.cpp
	${CC} -o $@ -I${INCLUDE_DIR} $^

${TARGET}_clean:
	rm -rfv ./${TARGET}