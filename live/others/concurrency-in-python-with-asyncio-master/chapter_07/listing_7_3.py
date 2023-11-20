import requests
from mpack.timer import timer

@timer
def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


url = "https://www.example.com"
results = [get_status_code(url) for _ in range(2)]
print(results[0], results[0].result)
print(results[1], results[1].result)