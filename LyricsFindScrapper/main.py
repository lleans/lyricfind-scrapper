from aiohttp import ClientSession

from .model import Track, SongData, Translation
from .const import LYRICSFIND_DOMAIN, get_param_search, get_param_translation
from .utils import get_build_id, get_current_ip, get_country_code


class LFException(Exception):
    def __init__(self, message: str = None, *, http_code: int = None) -> None:
        self.message = message
        self.http_code = http_code
        
        super().__init__(self._errors())

    def _errors(self):
        if self.http_code:
            http_error: dict = {
                404: "Not found",
                302: "Moved temporarily, or blocked by captcha",
                403: "Forbidden,or unvalid",
                429:  "Too many request",
                500: "Server error",
            }

            return http_error.get(self.http_code, f"Unknown error, please report to the project maintainer. HTTP code {self.http_code}")
        else:
            return f"Unknown error, please report to the project maintainer. HTTP code {self.message}"


class Search:
    def __init__(self, session=None, *, lib='asyncio', loop=None, teritory: str = None, limit: int = 5, **request_kwargs):
        self.request_kwargs = request_kwargs
        self.teritory: str = teritory
        self.limit: int = limit
        if lib not in ('asyncio'):
            raise ValueError(
                f"lib must be of type `str` and be either `asyncio' not '{lib if isinstance(lib, str) else lib.__class__.__name__}'")
        self._lib = lib
        if lib == 'asyncio':
            from asyncio import get_event_loop
            loop = loop or get_event_loop()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
        }
        self.session = session or ClientSession(loop=loop, headers=headers)

    async def get_tracks(self, query: str) -> 'list[Track]':
        if not self.teritory:
            ip: str = await get_current_ip(session=self.session)
            self.teritory = await get_country_code(session=self.session, ip=ip)

        params: dict = get_param_search(
            query=query, limit=self.limit, teritory=self.teritory)
        async with self.session.get(f"{LYRICSFIND_DOMAIN}api/v1/search", params=params) as resp:
            if resp.status < 400:
                data: dict = await resp.json()

                if data['tracks']:
                    return [Track(x) for x in data['tracks']]
                else:
                    raise LFException(http_code=resp.status)
            else:
                raise LFException(http_code=resp.status)

    async def get_lyrics(self, track: Track) -> SongData:
        slug: str = track.slug
        build_id: str = await get_build_id(session=self.session)
        url: str = f"{LYRICSFIND_DOMAIN}_next/data/{build_id}/en-US/lyrics/{slug}.json"

        async with self.session.get(url=url) as resp:
            if resp.status < 400:
                data: dict = await resp.json()

                return SongData(data=data['pageProps']['songData']['track'])
            else:
                raise LFException(http_code=resp.status)

    async def get_translation(self, track: Track, lang: str) -> Translation:
        if not track.available_translations:
            raise LFException(message="No translation found on this track!")

        lang = lang.lower()
        if not lang in track.available_translations:
            raise LFException(
                message=f"Please check the language you inputted!. Listed language {track.available_translations}(listed on array, select one))")

        url: str = f"{LYRICSFIND_DOMAIN}api/v1/translation"
        params: dict = get_param_translation(trackid=track.lfid, teritory=self.teritory, traslation_language=lang)
        async with self.session.get(url=url, params=params) as resp:
            if resp.status < 400:
                data: dict = await resp.json()
                return Translation(data=data['track'])
            else:
                raise LFException(http_code=resp.status)
