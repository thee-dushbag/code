CC=g++ -std=c++2b -Wall
INCLUDE_PATH=./include

main: templates.cpp
	${CC} -o $@ -I${INCLUDE_PATH} $^
