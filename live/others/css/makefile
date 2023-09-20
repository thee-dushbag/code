PORT=5052
HOST=192.168.0.100
HOST=localhost
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WORKER_CLASS=--worker-class ${WCLS}
BIND=--bind ${HOST}:${PORT}
OPTIONS=--reload ${BIND} ${WORKER_CLASS}
TARGET=main:application

all:
	@echo "Specify Server Type Please:"
	@echo "----> run serve  :for gunicorn heavy weigh server"
	@echo "----> run webrun :for aiohttp.run_app simple server"

serve:
	gunicorn ${OPTIONS} ${TARGET}

webrun:
	webrun ${BIND} ${TARGET}