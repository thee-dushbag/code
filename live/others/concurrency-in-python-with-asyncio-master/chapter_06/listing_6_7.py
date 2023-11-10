import time
from collections import defaultdict
from json import dump
freqs = defaultdict(lambda: 0)

with open("googlebooks-eng-all-1gram-20120701-a", encoding="utf-8") as f:
    start = time.time()

    for line in f:
        data = line.split("\t")
        word = data[0]
        count = int(data[2])
        freqs[word] += count

    end = time.time()
    print(f"{end-start:.4f}")

with open('n-gram.json', 'w') as f:
    dump(dict(freqs), f, indent=True)
