from pathlib import Path

CWD = Path.cwd()
dont_count = "users.db", "static", "__pycache__", "users.json"


def line_counter(file: Path):
    total_line_count = 0
    lines = len(tuple(filter(lambda line: line != "", file.read_text().splitlines())))
    print(f"{str(file.relative_to(CWD))!r:>30} -> {lines} lines.")
    total_line_count += lines
    return total_line_count


def dir_counter(path: Path):
    total_line_count = 0
    all_files = []
    for path in path.iterdir():
        if path.is_file() and path.name not in dont_count:
            total_line_count += line_counter(path)
            all_files.append(str(path.relative_to(CWD)))
        if path.is_dir() and path.name not in dont_count:
            files, count = dir_counter(path)
            all_files.extend(files)
            total_line_count += count
    return all_files, total_line_count


all_files, total_line_count = dir_counter(CWD)
print("All Files:", *all_files, sep="\n\t")
print(f"Total File Count: {len(all_files)}")
print(f"Total Line Count: {total_line_count}")
