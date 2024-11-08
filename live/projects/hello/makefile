CC_c=gcc -std=c2x -o3
CC_cpp=g++ -std=c++23 -o3
CC_rs=rustc -C opt-level=3
CC_py=pyinstaller
PY_BUILD_FILES=build dist main.spec

all: main_c main_cpp main_rs main_py

run: all
	ls -sh
	echo -n "Stat For main_c: "
	./main_c
	echo -n "Stat For main_cpp: "
	./main_cpp
	echo -n "Stat For main_rs: "
	./main_rs
	echo -n "Stat For main_py: "
	./main_py

main_c: main.c
	${CC_c} -o $@ $^

main_cpp: main.cpp
	${CC_cpp} -o $@ $^

main_rs: main.rs
	${CC_rs} -o $@ $^

main_py: main.py
	${CC_py} -F $^
	mv ./dist/main ./$@
	rm -rf ${PY_BUILD_FILES}
	clear

clean:
	rm -rf main_c main_cpp main_rs main_py ${PY_BUILD_FILES}
