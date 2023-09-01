PORT=5052
BIND=--bind ${STATICS_HOST}:${PORT}
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WCLASS_FLAG=--worker-class ${WCLS}
OPTIONS=--reload ${BIND} ${WCLASS_FLAG}
TARGET=main:application

serve:
	gunicorn ${OPTIONS} ${TARGET}