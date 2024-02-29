PORT=5052
BIND=--bind ${STATICS_HOST}:${PORT}
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WCLASS_FLAG=--worker-class ${WCLS}
OPTIONS=--reload ${BIND} ${WCLASS_FLAG}
TARGET=main:application

all: w

g: gunicorn_serve
w: webrun_serve

gunicorn_serve:
	gunicorn ${OPTIONS} ${TARGET}

webrun_serve:
	webrun ${BIND} ${TARGET}
