# CC=g++ -std=c++23
CC=clang++ -std=c++2b

.PHONY=clean lib pypow

main: usepow.cpp libpow.so
	${CC} -L. -lpow -Wl,-rpath=. -o $@ usepow.cpp

libpow.so: pow.hpp
	${CC} -shared -fpie -o $@ -x c++ $^

pypow.so: boost_pow.cpp
	${CC} -shared -fPIC -lboost_python3 -lpython3.11 -Wl,-soname,$@ -I/usr/include/python3.11 -o $@ $^

lib: libpow.so
pypow: pypow.so
clean:
	rm -rfv main libpow.so pypow.so
