import asyncio
import time
from pprint import pprint
from services.collecting_primary_data.get_21vek_data import get_21vek_data
from services.collecting_primary_data.get_kufar_data import get_kufar_data


def time_of_function(function):
    async def wrapped(*args):
        start_time = time.time()
        res = await function(*args)
        print(round(time.time() - start_time, 10))
        return res
    return wrapped

@time_of_function
async def run(query):
    data = await get_kufar_data(query, only_new=True)
    return data.products


for i in range(10):
    print(f'test: {i+1}')
    es = asyncio.run(run('realme'))
    pprint(es)
    print('\n')

