import aiohttp
import time
import asyncio
import asyncpg
from more_itertools import chunked

chunked_coros = 5

async def call_api(URL):
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as res:
            res_json= await res.json()
            return res_json



async def insert_data(pool: asyncpg.Pool, user_list):
    query = 'INSERT INTO herotable ( birth_year, eye_color, films, gender, hair_color, ' \
            'height, homeworld, mass, name, skin_color, species, starships, vehicles) ' \
            'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)'
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, user_list)

async def main():
    heros = await call_api('https://swapi.dev/api/people/')
    coros = []
    pool = await asyncpg.create_pool('postgresql://app:1234@127.0.0.1:5432/netology', min_size=20, max_size=20)
    tasks = []
    for y in range(heros['count']):
        call_api_coro = call_api(f'https://swapi.dev/api/people/{y+1}')
        coros.append(call_api_coro)
        count=1
    for drop_output in chunked(coros, chunked_coros):
        temp = []
        api_responses = await asyncio.gather(*drop_output)
        print(api_responses)
        for item in api_responses:
            try:
                items_tuple=(item['birth_year'], item['eye_color'], ('; '.join(item['films'])),
                             item['gender'], item['hair_color'], item['height'], item['homeworld'],
                             item['mass'], item['name'], item['skin_color'],('; '.join(item['species'])),
                             ('; '.join(item['starships'])), ('; '.join(item['vehicles'])))
                print(items_tuple)
                temp.append(items_tuple)
            except KeyError:
                pass
        print(temp)
        tasks.append(asyncio.create_task(insert_data(pool, temp)))
    await asyncio.gather(*tasks)
    await pool.close()





if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)