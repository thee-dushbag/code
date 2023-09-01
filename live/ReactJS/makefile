PORT=5052
BIND=--bind ${STATICS_HOST}:${PORT}
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WORKER_CLASS=--worker-class ${WCLS}
OPTIONS=--reload ${WORKER_CLASS} ${BIND}
TARGET=main:application

all:
	@echo run f/frontend :for serving react frontend
	@echo run r/run_app_backend :for serving aiohttp.run_app backend. Simple Server
	@echo run b/backend :for serving gunicorn heavy weigh backend

f: frontend
b:backend
r:run_app_backend

frontend:
	npm start

backend:
	gunicorn ${TARGET} ${OPTIONS}

run_app_backend:
	webrun ${BIND} ${TARGET}