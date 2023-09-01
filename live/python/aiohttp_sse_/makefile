PORT=5052
HOST=${STATICS_HOST}
BIND=--bind ${HOST}:${PORT}
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WORKER_CLASS=--worker-class ${WCLS}
G_OPTIONS=--reload ${BIND} ${WORKER_CLASS}
W_OPTIONS=
TARGET=main:application

serve: w_serve

w_serve:
	py -m aiohttp.web -H ${HOST} -P ${PORT} ${TARGET}

g_serve:
	gunicorn ${OPTIONS} ${TARGET}