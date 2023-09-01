HOST=localhost
PORT=5052
WCLASS=aiohttp.worker.GunicornUVLoopWebWorker

all:
	gunicorn web_site:app_factory --bind ${HOST}:${PORT} --reload --worker-class ${WCLASS}