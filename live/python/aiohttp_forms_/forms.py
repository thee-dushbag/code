from pathlib import Path
from random import randint
from typing import cast

from aiofiles import open as aopen
from aiohttp import web
from aiohttp.multipart import BodyPartReader, MultipartReader
from mpack import timer
from mpack.aiohttp_helpers.mako_ import setup, template

timer.FUNCTION_CALL_STR = "[{function_name}]"

files = [
    "File One",
    "File Two",
]

values = [
    # ("Name", "text"),
    # ("Email", "email"),
    # ("Password", "password"),
    *((file, "file") for file in files)
]

WORKING_DIR = Path.cwd()
STORE_DIR = WORKING_DIR / "store"
FILE_UPLOADS = STORE_DIR / "others"
TEMPLATE_DIR = STORE_DIR / "templates"


class FormData(web.View):
    @template("form.mako")
    async def get(self):
        return {"title": "This is a Test Form", "form_values": values}

    async def save_file(self, key: str, value: web.FileField):
        print(f"Saving File: {key!r}")
        file = FILE_UPLOADS / value.filename
        file.write_bytes(value.file.read())

    @timer.timer_async
    async def _multipart_file(self, name: str, obj: BodyPartReader):
        filename = FILE_UPLOADS / name
        # print(f"\t\tSaving File: {filename.name!r}")
        async with aopen(filename, "wb") as bfile:
            while chunk := await obj.read_chunk():
                await bfile.write(chunk)
        # with filename.open("wb") as bfile:
        #     while chunk := await obj.read_chunk():
        #         bfile.write(chunk)
        size = filename.stat().st_size
        # print(f"\t\tFile Saved: {filename.name!r} of {size=}")

    @timer.timer_async
    async def _deal_value(self, obj: BodyPartReader):
        if obj.name in files:
            d = str(randint(1, 1000)) + "__" + cast(str, obj.filename)
            if not d:
                return
            r = await self._multipart_file(d, obj)
            print(r)
            # await self._multipart_file(obj)
        else:
            d = await obj.text()
        # print(f"\t{obj.name} = {d!r}")

    @timer.timer_async
    async def deal_values(self, data: MultipartReader):
        async for obj in data:
            r = await self._deal_value(obj)
            print(r)

    async def post(self):
        data = await self.request.multipart()
        print("Received New Values:")
        result = await self.deal_values(data)
        print(result)
        raise web.HTTPSeeOther("/form")

    # async def post(self):
    #     data = await self.request.post()
    #     print("Received New Values:")
    #     task = []
    #     for key, value in data.items():
    #         if type(value) == web.FileField:
    #             task.append(aio.create_task(self.save_file(key, value)))
    #         print(f"\t{key} : {value!r}")
    #     if task: await aio.gather(*task)
    #     raise web.HTTPSeeOther("/form")


app = web.Application()
setup(app, str(TEMPLATE_DIR))
app.router.add_view("/form", FormData)
