import time
from concurrent.futures import ThreadPoolExecutor

import requests


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


start = time.time()

# urls = ("https://www.example.com" for _ in range(20))
# for url in urls:
#     print(get_status_code(url))

with ThreadPoolExecutor(max_workers=500) as pool:
    urls = ("https://www.example.com" for _ in range(500))
    results = pool.map(get_status_code, urls)
    for result in results:
        print(result)

end = time.time()

print(f"finished requests in {end - start:.4f} second(s)")
