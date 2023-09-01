CC=gcc -std=c2x -g -w

TARGET=main

all: ${TARGET}
	./${TARGET}

clean: ${TARGET}_clean

test: test.c
	${CC} -o $@ $^

test_clean:
	rm -rfv ./test

errors: errors.c
	${CC} -o $@ $^

errors_clean:
	rm -rfv ./errors

main: main.c
	${CC} -o $@ $^ -lpthread

main_clean:
	rm -rfv ./main