PATTERN = (
    r"""
(?P<scheme>[a-z]+)://
((?P<auth>
(?P<user>[a-z0-9.-]+):
(?P<password>[a-z0-9.-]+)?)@)?
(?P<host>[a-z0-9.-]+):(?P<port>\d+)
(?P<path>/?[/a-z0-9.]*)
(\#(?P<fragment>[a-z0-9.-]+))?
(\?(?P<query>[\w=&]+))?
"""
).replace("\n", "")
