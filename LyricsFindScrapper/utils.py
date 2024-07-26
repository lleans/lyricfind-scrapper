from aiohttp import ClientSession

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
