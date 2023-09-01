HOST=localhost
PORT=9999
FHOST=--host ${HOST}
FPORT=--port ${PORT}
WORKER_CLASS=aiohttp.worker.GunicornUVLoopWebWorker
GTARGET=apih:app
FTARGET=api:app
BIND_LOCATION=${HOST}:${PORT}
COMMON=--reload
GOPTIONS=--worker-class ${WORKER_CLASS} --bind ${BIND_LOCATION} ${COMMON}
FOPTIONS=${COMMON} ${FHOST} ${FPORT}

all: api

gcorn:
	gunicorn ${GOPTIONS} ${GTARGET}

api:
	uvicorn ${FOPTIONS} ${FTARGET}