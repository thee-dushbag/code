CUR_TARGET=templates_
CUR_TARGET=inhe_tmps_

MAKE_CMD=${MAKE} --quiet

main: main.cpp
	g++-12 -std=c++23 -fmodules-ts -o $@ $^ -I${HOME}/Content/code/lib/include

all: ${CUR_TARGET}
exe: ${CUR_TARGET}_exe
clean: ${CUR_TARGET}_clean

${CUR_TARGET}:
	${MAKE_CMD} --directory ${CUR_TARGET} all

${CUR_TARGET}_exe:
	${MAKE_CMD} --directory ${CUR_TARGET} exe

${CUR_TARGET}_clean:
	${MAKE_CMD} --directory ${CUR_TARGET} clean