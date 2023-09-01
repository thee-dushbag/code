WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WORKER_CLASS=--worker-class ${WCLS}
BIND=--bind ${MOVIE_HOST}:${MOVIE_PORT}
OPTS=--reload ${WORKER_CLASS} ${BIND}

serve: _preload _gcorn
serve_app: _preload _runapp

_preload:
	py ./preload/preload

_runapp:
	py main

_gcorn:
	gunicorn ${OPTS} main