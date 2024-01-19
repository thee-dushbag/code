import more_itertools as it
import dataclasses as dt
from aiohttp import web
import asyncio as aio
import textwrap as tw
import typing as ty


@dt.dataclass
class Email:
    receiver: str
    sender: str
    subject: str
    body: str

    def print(self):
        body = it.grouper(self.body, 42, incomplete="fill", fillvalue=" ")
        body = map("".join, body)
        body = "\n".join(body)
        body = tw.indent(body, "    ")
        lines = "-" * 50
        print("-" * 30 + "[ EMAIL ]" + "-" * 11)
        print(f"From: {self.sender}")
        print(f"To: {self.receiver}")
        print(f"Subject: {self.subject}")
        print(f"Body:\n{body}")
        print(lines)


async def process_emails(que: aio.Queue[Email]):
    print("EmailProcessor Up and Running.")
    try:
        while True:
            email = await que.get()
            que.task_done()
            if email is None:
                break
            email.print()
    except aio.CancelledError:
        ...
    finally:
        print("EmailProcessor Shutting down.")


EMAIL_QUEUE = "email.queue.my.app"


def get_equeue(app: web.Application) -> aio.Queue[Email]:
    q = app.get(EMAIL_QUEUE, None)
    if q is None:
        raise LookupError("Email queue was not setup.")
    return q


def get_emails(req: web.Request):
    return get_equeue(req.app)


async def setup_emails(app: web.Application):
    email_queue: aio.Queue[Email] = aio.Queue()
    app[EMAIL_QUEUE] = email_queue
    aio.create_task(process_emails(email_queue))
    yield
    email = ty.cast(Email, None)
    await email_queue.put(email)
    await email_queue.join()


async def email(req: web.Request):
    que = get_emails(req)
    subject = req.headers.get("Subject", None) or "<No Subject>"
    receiver = req.match_info.get("receiver", None) or "<No Receiver>"
    sender = req.match_info.get("sender", None) or "<No Sender>"
    body = req.headers.get("Body", None) or "<No Body>"
    if len(subject) > 30:
        raise web.HTTPBadRequest(
            body=f"Expected {subject!r} to be less than 31 characters."
        )
    email = Email(receiver, sender, subject, body)
    que.put_nowait(email)
    return web.Response(body=f"Email received successfully.")


def application():
    app = web.Application()
    app.cleanup_ctx.append(setup_emails)
    app.router.add_head(
        "/{sender:[a-zA-Z .-]{1,15}@[a-zA-Z.]{1,15}}"
        "/{receiver:[a-zA-Z .-]{1,15}@[a-zA-Z.]{1,15}}",
        email,
    )
    return app
