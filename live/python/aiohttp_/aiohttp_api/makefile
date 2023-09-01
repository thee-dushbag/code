PORT=5052
HOST=localhost
OPTIONS=--reload
WORKER_CLASS=--worker-class aiohttp.worker.GunicornUVLoopWebWorker
BIND=--bind ${HOST}:${PORT}
TARGET=main:app_factory

all:
	gunicorn ${OPTIONS} ${BIND} ${WORKER_CLASS} ${TARGET}