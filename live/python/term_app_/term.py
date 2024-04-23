import asyncio
from string import Template
from typing import Any, Callable, Protocol

from aiofiles.os import wrap  # type:ignore
from click import command

ainput = wrap(input)

CommandLike = Callable[["Term", str, tuple[str, ...], dict[str, str]], None]


class Command(Protocol):
    def __call__(
        self, term: "Term", command: str, args: tuple[str, ...], kwargs: dict[str, str]
    ): ...


class CommadNotFound:
    def __call__(
        self, term: "Term", command: str, args: tuple[str, ...], kwargs: dict[str, str]
    ):
        raise TermCommandNotFound(message=f"{command=} with {args=} was not found.")


class TermError(Exception):
    status = -1
    message = "Represents a Term Execution Status"

    def __init__(self, *args, pyex="", **kwargs) -> None:
        super().__init__(pyex)
        self.args = args
        self.kwargs = kwargs

    def to_term(self):
        return f"TermStatus with {self.args} and {self.kwargs}"


class TermArgsError(TermError):
    status = 1
    message = "Arg Parsing Error"

    def to_term(self):
        a = self.kwargs.get("args")
        k = self.kwargs.get("kwargs")
        s = self.kwargs.get("sargs")
        return f"Unable to decode args and kwargs[{s}]: {a} {k}"


class TermSuccess(TermError):
    status = 0
    message = "Command Run Successfully"

    def to_term(self):
        output: str | None = self.kwargs.get("message")
        return output or ""


class TermCommandNotFound(TermError):
    status = 3
    message = "Command Was Not Found"

    def to_term(self):
        output: str | None = self.kwargs.get("message")
        return output or ""


class TermTemplateError(TermError):
    status = 2
    message = "Template Arg Error"

    def to_term(self):
        context = self.kwargs.get("context")
        arg = self.kwargs.get("arg")
        return f"Undefined variable {arg!r} used in {context}"


class TermKwargsNotAllowed(TermError):
    status = 5
    message = "When Kwargs are not permitted in command"

    def to_term(self):
        sargs = self.kwargs.get("skwargs")
        command = self.kwargs.get("command")
        return f"Kwargs Not Allowed: {sargs} in {command=}: USE ARGS"


class TermArgsNotAllowed(TermError):
    status = 4
    message = "When Args are not permitted in command"

    def to_term(self):
        sargs = self.kwargs.get("sargs")
        command = self.kwargs.get("command")
        return f"Args Not Allowed: {sargs} in {command=}: USE KWARGS"


class TermValueNotDefined(TermError):
    status = 6
    message = "When Operating with unset values"

    def to_term(self):
        und = self.kwargs.get("undefined")
        return f"Bindings {und} were not found."


class ExitTerm:
    def __call__(self, term: "Term", *args: Any, **kwds: Any) -> Any:
        loop = asyncio.get_event_loop()
        tasks = asyncio.all_tasks(loop)
        [task.cancel() for task in tasks]
        term.running = False


class SetValue:
    def __call__(self, term: "Term", cmd, args: Any, kwds: Any) -> Any:
        if args:
            raise TermArgsNotAllowed(command=cmd, sargs=" ".join(args))
        term.namespace.update(kwds)


class GetValue:
    def __call__(self, term: "Term", cmd, args: Any, kwds: Any) -> Any:
        args = [arg for arg in args if arg]
        for arg in args if args else term.namespace:
            if not arg:
                continue
            value = term.namespace.get(arg, "'Not Defined'")
            print(f"--{arg}={value}")
        raise TermSuccess


class DelValue:
    def __call__(self, term: "Term", cmd: str, args: Any, kwds: Any) -> Any:
        if kwds:
            skwargs = " ".join(f"--{k}={v}" for k, v in kwds.items())
            raise TermKwargsNotAllowed(skwargs=skwargs, command=cmd)
        undefined = []
        for arg in args:
            if arg not in term.namespace:
                undefined.append(arg)
            else:
                term.namespace.pop(arg)


class SayHiTestCommand:
    def __call__(self, term: "Term", cmd, args: Any, kwds: Any) -> Any:
        if kwds:
            skwargs = " ".join(f"--{k}={v}" for k, v in kwds.items())
            raise TermKwargsNotAllowed(skwargs=skwargs, command=cmd)
        for name in args:
            print(f"Hello {name}, how was your day?")
        raise TermSuccess(message=f"Greeted: {list(args)}")


class Term:
    def __init__(self, prompt) -> None:
        self.commands: dict[str, CommandLike] = {}
        self.commands["sayhi"] = SayHiTestCommand()
        self.commands["exit"] = ExitTerm()
        self.commands["set"] = SetValue()
        self.commands["del"] = DelValue()
        self.commands["get"] = GetValue()
        self._no_cmd = CommadNotFound()
        self.prompt: str = prompt
        self.running = False
        self.namespace = {}

    async def run_forever(self):
        if self.running:
            return
        self.running = True
        while self.running:
            await self.get_command()

    async def get_command(self):
        cmd = await ainput(self.prompt)
        # cmd = input(self.prompt)
        command, sargs = self.split_command(cmd)
        await self.run_command(command, sargs)

    async def render_args(self, sargs: str):
        tmp = Template(sargs)
        try:
            sargs = tmp.substitute(**self.namespace)
        except KeyError as e:
            raise TermTemplateError(context=sargs, arg=str(e))
        else:
            return sargs

    async def make_args(self, sargs: str):
        args, kwargs = [], {}

        async def split_kwarg_arg(arg: str):
            try:
                k = arg.strip("-")
                key, value = k.split("=")
            except Exception:
                raise TermArgsError(kwargs=[arg], sargs=sargs)
            else:
                return key, value

        async def arg_type(arg: str):
            if arg.startswith("--"):
                key, value = await split_kwarg_arg(arg)
                kwargs[key] = value
            else:
                args.append(arg)

        pieces = sargs.split(" ")
        for piece in pieces:
            await arg_type(piece)
        return tuple(arg for arg in args if arg), kwargs

    def split_command(self, cmd: str):
        cmd, _, args = cmd.partition(" ")
        return cmd, args

    async def run_command(self, cmd, sargs):
        command = self.commands.get(cmd, self._no_cmd)
        status: TermError
        try:
            sargs = await self.render_args(sargs)
            args, kwargs = await self.make_args(sargs)
            res = command(self, cmd, args, kwargs)
            status = TermSuccess(message=str(res))
        except Exception as e:
            if not issubclass(type(e), TermError):
                e = TermError(str(e))
            status = e  # type:ignore
        if status.status != 0:
            print(f"Output: {status.to_term()}")
            print(f"Status: {status.status}")

    def make_command(self, command_name: str):
        def make_callable_cmd(func: CommandLike):
            self.commands[command_name] = func

        return make_callable_cmd
