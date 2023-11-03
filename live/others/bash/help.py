from mpack.number_reader import get_reader
from pathlib import Path
from string import Template
from mpack.stream import Stream

reader = get_reader('english')
line_template = Template('This is line $word.')
filename = Path.cwd() / 'text.txt'

with filename.open('w') as file:
    with Stream(out_stream=file):
        for i in range(1, 10):
            print(line_template.substitute(word=reader(i)))