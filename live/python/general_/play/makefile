CODE_DIR=`pwd`

LIVE_DIR=${CODE_DIR}/live
LIB_DIR=${CODE_DIR}/lib

PYTHON_DIR=${LIVE_DIR}/python
CPP_DIR=${LIVE_DIR}/c++
C_DIR=${LIVE_DIR}/c
MATH_DIR=${LIVE_DIR}/math
RUST_DIR=${LIVE_DIR}/rust
JAVASCRIPT_DIR=${LIVE_DIR}/javascript
TYPESCRIPT_DIR=${LIVE_DIR}/typescript
OTHERS=${LIVE_DIR}/others

MAKE_CMD=${MAKE} --quiet

TARGET_DIR=${PYTHON_DIR}

.PHONY=main clean all

all: main

main:
	${MAKE_CMD} --directory ${TARGET_DIR} all

exe:
	${MAKE_CMD} --directory ${TARGET_DIR} exe

clean:
	${MAKE_CMD} --directory ${TARGET_DIR} clean
