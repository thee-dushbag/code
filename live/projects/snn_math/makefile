CC=gcc -std=c17 -w -g

#Resource Directories.
MAIN_DIR=.
INCLUDE_PATH=${MAIN_DIR}/include
LIBRARY_PATH=${MAIN_DIR}/lib

#Adding Resource Directories to the Search Path
VPATH=${LIBRARY_PATH} ${INCLUDE_PATH}
.PHONY=basic_clean run clean

run: main math
	make basic_clean

math: math.o libsnnmath.so
	${CC} -o $@ math.o -L${LIBRARY_PATH} -Wl,-rpath,${LIBRARY_PATH} -lsnnmath

main: main.o libsnnmath.so
	${CC} -o $@ main.o -L${LIBRARY_PATH} -Wl,-rpath,${LIBRARY_PATH} -lsnnmath

math.o: math.c
	${CC} -c -o $@ $^ -I${INCLUDE_PATH}

main.o: main.c
	${CC} -c -o $@ $^ -I${INCLUDE_PATH}

libsnnmath.so: snn_math_impl.o
	${CC} -shared -fPIC -o ${LIBRARY_PATH}/$@ ${LIBRARY_PATH}/$^

snn_math_impl.o: snn_math_impl.h
	${CC} -o ${LIBRARY_PATH}/$@ -x c -c $^

clean: basic_clean
	rm -rf ${LIBRARY_PATH}/*.so
	rm -rf ${MAIN_DIR}/main
	rm -rf ${MAIN_DIR}/math

basic_clean:
	rm -rf ${MAIN_DIR}/*.o
	rm -rf ${LIBRARY_PATH}/*.o