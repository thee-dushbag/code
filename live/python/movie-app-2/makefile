PORT=9080
HOST=${STATICS_HOST}
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WORKER_CLASS=--worker-class ${WCLS}
BIND=--bind ${HOST}:${PORT}
OPTIONS=--reload ${WORKER_CLASS} ${BIND}
TARGET=main:application

.PHONY=all:s:g:a:gunicorn_serve:aiohttp_serve:statics

all:
	@echo Please use the preferred commands:
	@echo run gunicorn_serve/g  :Gunicorn heavyweigh server
	@echo run aiohttp_serve/a   :Aiohttp webrun lite server

g: gunicorn_serve
a: aiohttp_serve

gunicorn_serve:
	gunicorn ${TARGET} ${OPTIONS}

aiohttp_serve:
	webrun ${TARGET} ${BIND}