PORT=5052
HOST=192.168.0.100
WCLS=aiohttp.worker.GunicornUVLoopWebWorker
WORKER_CLASS=--worker-class ${WCLS}
BIND=--bind ${HOST}:${PORT}
OPTIONS=--reload ${BIND} ${WORKER_CLASS}

TARGET=test:application

main: main.cpp
	g++-13 -std=c++23 -o main main.cpp

serve:
	gunicorn ${OPTIONS} ${TARGET}