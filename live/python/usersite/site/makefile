APP = app
HOST = localhost
PORT = 5052
WORKER_CLASS = aiohttp.worker.GunicornWebWorker
RUNNER = gunicorn

runserver: main.py
	${RUNNER} --reload --bind ${HOST}:${PORT} --worker-class ${WORKER_CLASS} main:${APP}