PORT=5052
BIND=--bind ${STATICS_HOST}:${PORT}
WCLASS=--worker-class aiohttp.worker.GunicornUVLoopWebWorker
OPTIONS=--reload ${BIND} ${WCLASS}
TARGET=main:application

all:
	gunicorn ${OPTIONS} ${TARGET}
