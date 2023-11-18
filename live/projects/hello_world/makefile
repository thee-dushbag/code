.PHONY=main run tmain trun

all:
	echo Choose either main or tmain

main: mainc maincpp mainrs
	echo -n

run: main
	./mainc
	./maincpp
	./mainrs

mainc: main.c
	gcc -O3 -std=c2x -o $@ $^

maincpp: main.cpp
	g++ -O3 -std=c++23 -o $@ $^

mainrs: main.rs
	rustc -o $@ $^

tmain: tmainc tmaincpp tmainrs

trun: tmain
	./time ./tmainc
	./time ./tmaincpp
	./time ./tmainrs

tmainc: main.c
	./time gcc -O3 -std=c2x -o $@ $^

tmaincpp: main.cpp
	./time g++ -O3 -std=c++23 -o $@ $^

tmainrs: main.rs
	./time rustc -o $@ $^

clean:
	rm -rfv {t,}main{c,cpp,rs}