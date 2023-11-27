from datetime import datetime, timedelta
from json import loads, dumps

from aiohttp import ClientSession
from pyquery import PyQuery

from .const import IP_LOCATION_API, LYRICSFIND_DOMAIN


async def get_current_ip(session: ClientSession) -> str:
    async with session.get(IP_LOCATION_API, params={'cmd': 'get-ip'}) as resp:
        if resp.status == 200:
            data: dict = await resp.json()
            return data.pop('ip')

        return '1.1.1.1'


async def get_country_code(session: ClientSession, ip: str) -> str:
    async with session.get(IP_LOCATION_API, params={'ip': ip}) as resp:
        if resp.status == 200:
            data: dict = await resp.json()
            return data.pop('country_code2')

        return 'US'


async def get_build_id(session: ClientSession) -> str:
    expired_days: int = 7

    filename: str = 'build_id'
    build_id: str
    build_date: datetime

    async def get_new() -> str:
        async with session.get(LYRICSFIND_DOMAIN) as build:
            data: PyQuery = PyQuery(await build.text(encoding='utf-8'))('head script').eq(-2)
            return str(data.attr('src')).split('/')[3]

    with open(f'{filename}.json', 'w+') as file:
        try:
            loaded: dict = loads(file.read())
            build_id = loaded.get('build_id')
            build_date = loaded.get('build_date')

            current_utc: datetime = datetime.utcnow()

            if build_id and build_date and datetime.utcfromtimestamp(build_date) > current_utc:
                return build_id
            else:
                raise Exception("Renew")
        except:
            build_id = await get_new()
            build_date = int(
                (datetime.utcnow() + timedelta(days=expired_days)).timestamp())
            loaded = {
                'build_id': build_id,
                'build_date': build_date
            }

            file.seek(0)
            file.truncate()

            file.write(dumps(loaded))
            return build_id
