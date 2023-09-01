HOST=localhost
PORT=5052
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WORKER_CLASS=--worker-class ${WCLS}
BIND=--bind ${HOST}:${PORT}
OPTS=--reload ${WORKER_CLASS} ${BIND}

all:
	gunicorn ${OPTS} main