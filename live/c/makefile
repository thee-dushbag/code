CUR_TARGET=general_

MAKE_CMD=${MAKE} --quiet -B

all: ${CUR_TARGET}
clean: ${CUR_TARGET}_clean

general_:
	${MAKE_CMD} --directory ${CUR_TARGET} all

general__clean:
	${MAKE_CMD} --directory ${CUR_TARGET} clean