APP=app
HOST=localhost
PORT=5052
WORKER_CLASS=aiohttp.worker.GunicornWebWorker
RUNNER=gunicorn
MODULE=test_site

runserver: ${MODULE}.py
	${RUNNER} --reload --bind ${HOST}:${PORT} --worker-class ${WORKER_CLASS} ${MODULE}:${APP} --reload-extra-file ./templates/page.html --reload-extra-file ./templates/base.html --reload-extra-file ./templates/pages.html --reload-extra-file ./templates/utils.html
