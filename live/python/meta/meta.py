import typing as ty

T = ty.TypeVar("T")
Transformer = ty.Callable[[T], T]


def indent_str(indent: str | None = None) -> Transformer[str]:
    indent = "    " if indent is None else indent
    return lambda line: indent + line


def append_char(char: str | None = None) -> Transformer[str]:
    char = "\n" if char is None else char
    return lambda string: string + char


def with_append(content: ty.Iterable[str], char: str | None = None):
    return map(append_char(char), content)


def with_indent(content: ty.Iterable[str], indent: str | None = None):
    return map(indent_str(indent), content)


def create_function(
    name: str,
    args: ty.Iterable[str],
    body: ty.Iterable[str],
    ret_type: str | None = None,
) -> ty.Generator[str, None, None]:
    arg = ", ".join(args)
    ret_type = f" -> {ret_type}" if ret_type else ""
    yield f"def {name}({arg}){ret_type}:"
    yield from with_indent(body)


def create_class(
    name: str, bases: ty.Iterable[str], body: ty.Iterable[str]
) -> ty.Generator[str, None, None]:
    _base = ", ".join(bases)
    base = f"({_base})" if _base else ""
    yield f"class {name}{base}:"
    yield from with_indent(body)


def imports(import_: str, from_: str | None = None, as_: str | None = None):
    import_ = f"import {import_}"
    if as_ is not None:
        import_ = f"{import_} as {as_}"
    if from_ is not None:
        import_ = f"from {from_} {import_}"
    return import_


def import_from(from_: str, *names: str | tuple[str, str]):
    for name in names:
        match name:
            case tuple():
                iname, alias = name
            case str():
                iname, alias = name, None
            case _:
                ty.assert_never(name)
        yield imports(iname, from_, alias)


def module(
    *sources: ty.Iterable[str | ty.Iterable[str] | str],
) -> ty.Generator[str, None, None]:
    for body in sources:
        if isinstance(body, str):
            yield body
            continue
        for line in body:
            if isinstance(line, str):
                yield line
                continue
            yield from line


def join(thing, things: ty.Iterable):
    it = iter(things)
    try:
        yield next(it)
    except StopIteration:
        ...
    else:
        for obj in it:
            yield thing
            yield obj
