from aiohttp import web
import processor  # Import our processor plugin

CTX_TYPE = 'ctx' # Contol which type of setup-teardown is used. ctx/seted

async def process_order(req: web.Request):
    queue = req.app[processor.QUEUE]
    task = next(processor.GENERATOR)  # Get a task
    await queue.put(task)  # Add task to be processed
    return web.Response(body=f"Order placed: {task}")


routes = [web.get("/order", process_order)]


async def application():
    app = web.Application()
    processor.setup(app, CTX_TYPE)  # Install plugin
    app.add_routes(routes)
    return app


if __name__ == "__main__":
    try:
        web.run_app(application())
        # Remember to press Ctrl+C to stop the application
        # when there are some tasks on queue to see the effect
        # of the setup-teardown.
    except KeyboardInterrupt:
        ...
