PORT=5052
BIND=--bind ${STATICS_HOST}:${PORT}
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WORKER_CLASS=--worker-class ${WCLS}
OPTIONS=--reload ${WORKER_CLASS} ${BIND}
TARGET=main:application

all:

b:backend
r:run_app_backend

backend:
	gunicorn ${TARGET} ${OPTIONS}

run_app_backend:
	py ./webrun ${PORT}