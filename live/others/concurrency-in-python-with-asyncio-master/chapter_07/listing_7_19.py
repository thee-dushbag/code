import asyncio
import numpy as np
from util import async_timed

data_points = 250_000_000
rows = 50
columns = int(data_points / rows)

matrix = np.arange(data_points).reshape(rows, columns)

@async_timed()
async def main():
    mean_for_row = lambda row: np.mean(matrix[row])
    tasks = (asyncio.to_thread(mean_for_row, row) for row in range(rows))
    await asyncio.gather(*tasks)

asyncio.run(main())
