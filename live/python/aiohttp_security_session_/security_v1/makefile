all:
	gunicorn --bind localhost:5052 --reload --worker-class aiohttp.worker.GunicornWebWorker main:app
