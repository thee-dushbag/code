CC=g++ -std=c++23 -g -I. -w
VPATH=/usr/include/c++/12

TARGET=main
.PHONY=all clean

all: ${TARGET} exe

clean: ${TARGET}_clean

exe:
	./${TARGET}

main: main.cpp
	${CC} -o $@ $^

main_clean:
	rm -rfv ./main