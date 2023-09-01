PORT=5052
HOST=localhost
HOST=192.168.0.100
BIND=--bind ${HOST}:${PORT}
WCLASS=--worker-class aiohttp.worker.GunicornUVLoopWebWorker
OPTIONS=--reload
TARGET=main:app_factory

all:
	gunicorn ${BIND} ${OPTIONS} ${WCLASS} ${TARGET}