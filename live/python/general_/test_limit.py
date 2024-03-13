from subprocess import run, CalledProcessError
from string import ascii_letters, digits
import typing as ty, os, click
from tempfile import mktemp


valid_identifier_chars = set(ascii_letters + digits + "_")
headers = "#include <iostream>\n"
struct_template = "struct %s { volatile int value; };"
p_operator = """std::ostream &
operator<<(std::ostream &out, %s const &_)
{ return out << "%s"; }
"""


def main_function(count: int, *body_parts):
    yield "int main() {\n"
    for part in body_parts:
        yield from part
    yield 'std::cout << "Created %s classes.\\n";\n' % count
    yield "return 0; }\n"


def instantiate(base_name: str, count: range):
    for cid in count:
        yield f"{base_name}{cid} instance{cid};"


def print_operator(base_name: str, count: range):
    clsname = lambda cid: base_name + str(cid)
    for name in map(clsname, count):
        yield p_operator % (name, name)


def print_instances(base_name: str, count: range):
    for cid in count:
        yield f"std::cout << instance{cid} << '\\n';"


def create_struct(base_name: str):
    def create(cid: int | str):
        name = base_name + str(cid)
        return struct_template % name

    return create


def create_cpp_source(base_name: str, count: int):
    r = range(1, count + 1)
    nl = lambda s: s + "\n"
    yield headers
    mystruct = create_struct(base_name)
    yield from map(nl, (mystruct(i) for i in r))
    yield from print_operator(base_name, r)
    idecl = map(nl, instantiate(base_name, r))
    iprints = map(nl, print_instances(base_name, r))
    yield from main_function(count, idecl, iprints)


def write_cpp_source(file: ty.IO[str], base_name: str, count: int):
    for line in create_cpp_source(base_name, count):
        file.write(line)


def create_cpp_file(filename: str, base_name: str, count: int):
    with open(filename, "w") as file:
        write_cpp_source(file, base_name, count)


def compile_cpp_file(filename: str, output: str):
    return run(["g++", "-xc++", "-O3", "-o", output, filename], check=True).returncode


def create_ncompile(output: str, base_name: str, count: int):
    filename = mktemp()
    try:
        create_cpp_file(filename, base_name, count)
        print("Source size:", os.stat(filename).st_size, "bytes.")
        return compile_cpp_file(filename, output)
    finally:
        os.remove(filename)


def create_compile_nrun(base_name: str, count: int):
    output = mktemp()
    try:
        ecode = create_ncompile(output, base_name, count)
        print("Executable size:", os.stat(output).st_size, "bytes.")
        os.chmod(output, 100)
        run(output)
        os.remove(output)
        return ecode
    except CalledProcessError as e:
        print(f"Command: {e.cmd} failed.")
        return e.returncode


def validate_variable_name(ctx: click.Context, param: click.Parameter, value: str):
    if not value:
        raise click.BadParameter("Empty name is not acceptable.", ctx, param)
    if value[0].isdigit():
        raise click.BadParameter("Name cannot start with a digit.")
    if invalid := (set(value) - valid_identifier_chars):
        raise click.BadParameter(str(invalid), ctx, param)
    return value


@click.command
@click.option(
    "--base-name", "-b", callback=validate_variable_name, type=str, default="Type"
)
@click.argument("count", required=False, default=10, type=int)
@click.pass_context
def main(ctx: click.Context, count: int, base_name: str):
    ctx.exit(create_compile_nrun(base_name, count))


if __name__ == "__main__":
    main()
