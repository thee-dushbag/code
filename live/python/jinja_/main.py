from asyncio import run

from faker import Faker
from jinja2 import (ChoiceLoader, DictLoader, Environment, FileSystemLoader,
                    PackageLoader, select_autoescape)

fake = Faker()

pack_loader = PackageLoader("pack")
env = Environment(
    loader=pack_loader,
    autoescape=select_autoescape(["html", "xml"]),
    auto_reload=False,
    line_statement_prefix="#"
    # enable_async=True,
)
render_names = env.get_template("template")
names = *(fake.name() for _ in range(10)), "Simon<Nganga"
html_names = render_names.render(names=names)
print(html_names)
