TARGET=main
TARGET=dbtest
APP_TARGET=app_factory
HOST=192.168.0.100
PORT=5052
WCLS=aiohttp.worker.GunicornWebWorker
BIND=--bind ${HOST}:${PORT}
CLASS=--worker-class ${WCLS}
OPTIONS=--reload ${BIND} ${CLASS}

.PHONY=all run serve

all: run

run:
	py ${TARGET}

serve:
	gunicorn ${OPTIONS} ${TARGET}:${APP_TARGET}