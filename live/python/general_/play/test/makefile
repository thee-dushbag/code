HOST=192.168.0.100
PORT=5052

WORKER_CLASS=aiohttp.worker.GunicornUVLoopWebWorker
WCLASS_OPT=--worker-class ${WORKER_CLASS}
BIND=${HOST}:${PORT}
BIND_OPT=--bind ${BIND}

OPTIONS=--reload ${BIND_OPT} ${WCLASS_OPT}
TARGET=main:app_factory

all:
	gunicorn ${OPTIONS} ${TARGET}