from jinja2 import (
    Environment,
    FileSystemLoader,
    ChoiceLoader,
    DictLoader,
    PackageLoader,
    select_autoescape,
)
from asyncio import run
from faker import Faker

fake = Faker()

pack_loader = PackageLoader("pack")
env = Environment(
    loader=pack_loader,
    autoescape=select_autoescape(["html", "xml"]),
    auto_reload=False,
    line_statement_prefix='#'
    # enable_async=True,
)
render_names = env.get_template("template")
names = *(fake.name() for _ in range(10)), "Simon<Nganga"
html_names = render_names.render(names=names)
print(html_names)