CC=g++ -std=c++23 -g -I. -w

TARGET=main
.PHONY=all clean

all: ${TARGET} exe

clean: ${TARGET}_clean

exe:
	./${TARGET}

${TARGET}: ${TARGET}.cpp
	${CC} -o $@ -I/home/simon/Content/code/lib/include $^

${TARGET}_clean:
	rm -rfv ./${TARGET}