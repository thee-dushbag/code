import asyncio, typing as ty, logging, aiohttp, aiohttp.web

PRODUCT_BASE = "http://127.0.0.1:8000"
INVENTORY_BASE = "http://127.0.0.1:8001"
FAVORITE_BASE = "http://127.0.0.1:8002"
CART_BASE = "http://127.0.0.1:8003"


async def all_products(req: aiohttp.web.Request) -> aiohttp.web.Response:
    async with aiohttp.ClientSession() as sess:
        products = asyncio.create_task(sess.get(f"{PRODUCT_BASE}/products"))
        favorites = asyncio.create_task(sess.get(f"{FAVORITE_BASE}/users/3/favorites"))
        cart = asyncio.create_task(sess.get(f"{CART_BASE}/users/3/cart"))

        requests = [products, favorites, cart]
        done, pending = await asyncio.wait(requests, timeout=1.0)

        if products in pending:
            [request.cancel() for request in requests]
            return aiohttp.web.json_response({"error": "Could not reach products service."}, status=504)

        elif products in done and products.exception() is not None:
            [request.cancel() for request in requests]
            logging.exception("Server error reaching product service.", exc_info=products.exception())
            return aiohttp.web.json_response({"error": "Server error reaching products service."}, status=500)
        else:
            product_response = await products.result().json()
            product_results: list[dict] = await get_products_with_inventory(sess, product_response)
    
            cart_item_count: ty.Optional[int] = await get_response_item_count(
                cart, done, pending, "Error getting user cart.")
        
            favorite_item_count: ty.Optional[int] = await get_response_item_count(
                favorites, done, pending, "Error getting user favorites.")

            return aiohttp.web.json_response({
                "cart_items": cart_item_count,
                "favorite_items": favorite_item_count,
                "products": product_results,
            })


async def get_products_with_inventory(sess: aiohttp.ClientSession, product_response) -> list[dict]:
    def get_inventory(sess: aiohttp.ClientSession, product_id: str) -> asyncio.Task:
        url = f"{INVENTORY_BASE}/products/{product_id}/inventory"
        return asyncio.create_task(sess.get(url))

    def create_product_record(product_id: int, inventory: ty.Optional[int]) -> dict:
        return {"product_id": product_id, "inventory": inventory}

    inventory_tasks_to_product_id = {
        get_inventory(sess, product["product_id"]): product["product_id"]
        for product in product_response
    }

    inventory_done, inventory_pending = await asyncio.wait(
        inventory_tasks_to_product_id.keys(), timeout=1.0)

    product_results = []

    for done_task in inventory_done:
        if done_task.exception() is None:
            product_id = inventory_tasks_to_product_id[done_task]
            inventory = await done_task.result().json()
            product_results.append(create_product_record(product_id, inventory["inventory"]))
        else:
            product_id = inventory_tasks_to_product_id[done_task]
            product_results.append(create_product_record(product_id, None))
            logging.exception(
                f"Error getting inventory for id {product_id}",
                exc_info=inventory_tasks_to_product_id[done_task].exception())

    for pending_task in inventory_pending:
        pending_task.cancel()
        product_id = inventory_tasks_to_product_id[pending_task]
        product_results.append(create_product_record(product_id, None))

    return product_results


async def get_response_item_count(
    task: asyncio.Task,
    done: set[asyncio.Task],
    pending: set[asyncio.Task],
    error_msg: str
) -> ty.Optional[int]:
    if task in done and task.exception() is None:
        return len(await task.result().json())
    elif task in pending: task.cancel()
    else: logging.exception(error_msg, exc_info=task.exception())
    return None


routes = [aiohttp.web.get("/products/all", all_products)]


async def application() -> aiohttp.web.Application:
    app = aiohttp.web.Application()
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    aiohttp.web.run_app(application(), port=9000)
