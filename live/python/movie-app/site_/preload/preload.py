import os
from pathlib import Path

import yaml
from css_html_js_minify import process_single_css_file, process_single_js_file

PRELOAD_DIR = Path(__file__).parent
P_DIR = Path(os.getcwd())
os.chdir(PRELOAD_DIR)

with open(PRELOAD_DIR / "targets.yaml") as file:
    targets = yaml.safe_load(file)["targets"]


def process_file(input, output):
    if Path(input).suffix == ".css":
        process_single_css_file(input, overwrite=True, output_path=output)
    elif Path(input).suffix == ".js":
        process_single_js_file(input, overwrite=True, output_path=output)
    else:
        print(f"Processor for {input} was not found")


for target in targets:
    process_file(**target)

os.chdir(P_DIR)
