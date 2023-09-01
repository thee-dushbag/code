all: index
clean:
exe: index

index: index.js
	nodejs $^

serve:
	gunicorn --reload --worker-class aiohttp.worker.GunicornUVLoopWebWorker --bind ${STATICS_HOST}:5052 server:application