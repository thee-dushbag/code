BIND=--bind ${STATICS_HOST}:${STATICS_PORT}
WCLASS=--worker-class aiohttp.worker.GunicornUVLoopWebWorker
OPTIONS=--reload
TARGET=main:app_factory


all: serve

run_app:
	python3 main

serve:
	gunicorn ${BIND} ${OPTIONS} ${WCLASS} ${TARGET}