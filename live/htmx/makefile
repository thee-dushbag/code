PORT=5052
HOST=localhost
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
OPTIONS=--reload ${BIND} ${WORKER_CLASS}
WORKER_CLASS=--worker-class ${WCLS}
BIND=--bind ${HOST}:${PORT}
TARGET=main:application

.PHONY=s:serve

s: serve

serve:
	gunicorn ${OPTIONS} ${TARGET}