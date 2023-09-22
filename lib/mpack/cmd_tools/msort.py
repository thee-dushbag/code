from pathlib import Path

import click as _c


@_c.command
@_c.option(
    "--file",
    "-i",
    help="File to sort its lines.",
    type=_c.Path(exists=True, dir_okay=False),
)
@_c.option(
    "--print0", help=r"Output file delimeter is \0 instead of newlines \n", is_flag=True
)
@_c.option(
    "--scan0", help=r"Input file delimeter is \0 instead of newlines \n", is_flag=True
)
@_c.option("--reverse", "-r", help="Reverse the sort order", is_flag=True)
@_c.option("--output", "-o", help="File to write the sorted output")
def msort(reverse: bool, file: str, output: str, scan0: bool, print0: bool):
    """Sort a list of strings."""
    indelim = "\0" if scan0 else "\n"
    outdelim = "\0" if print0 else "\n"
    if file:
        data = Path(file).read_text()
    else:
        data = input()
    sorteddata = data.split(indelim)
    sorteddata.sort(reverse=reverse)
    data = outdelim.join(sorteddata)
    if not output:
        return _c.echo(data)
    path = Path(output)
    if not path.exists():
        path.touch()
    path.write_text(data)
