from aiohttp import web
from pathlib import Path
from attrs import define, asdict, field
import json
from functools import partial
import asyncio as aio


MSG_KEY = 'messages.app.key'
MSG_FILE = 'messages.json'

@define(kw_only=True)
class UserMsg:
    sender: str
    message: str

MsgCont = list[UserMsg]

@define
class MessageManager:
    messages: MsgCont = field(factory=list)
    message_queue: aio.Queue[UserMsg] = field(init=False, factory=aio.Queue)

    async def add(self, message: UserMsg):
        self.messages.append(message)
        await self.message_queue.put(message)

async def save_messages(app: web.Application, path: Path):
    message_manager: MessageManager = app[MSG_KEY]
    user_msgs = message_manager.messages
    msgs = [asdict(msg) for msg in user_msgs]
    content = json.dumps({MSG_KEY: msgs})
    path.write_text(content)

async def load_messages(app: web.Application, path: Path):
    if not path.exists(): path.touch()
    content = path.read_text() or '{}'
    jmsgs = json.loads(content)
    msgs = jmsgs.get(MSG_KEY, [])
    user_msgs: MsgCont = [UserMsg(**msg) for msg in msgs]
    message_manager = MessageManager(user_msgs)
    app[MSG_KEY] = message_manager

def get_messages_from_app(app: web.Application) -> MessageManager:
    message_manager: None | MessageManager = app.get(MSG_KEY, None)
    assert isinstance(message_manager, MessageManager),\
        'Call store.setup on your application.'
    return message_manager

def get_messages(req: web.Request):
    return get_messages_from_app(req.app)

async def msg_ctx(app: web.Application, path: Path):
    await load_messages(app, path)
    yield
    await save_messages(app, path)


def setup(app: web.Application, path: Path | str | None=None):
    _path = path or MSG_FILE
    _msg_ctx = partial(msg_ctx, path=Path(str(_path)))
    app.cleanup_ctx.append(_msg_ctx)