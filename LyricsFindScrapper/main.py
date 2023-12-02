from aiohttp import ClientSession

from .model import Track, SongData, Translation
from .const import LYRICSFIND_DOMAIN, Param
from .utils import get_current_ip, get_country_code


class LFException(Exception):
    def __init__(self, message: str = None, was_generic: bool = False, *, http_code: int = None) -> None:
        self.message = message
        self.http_code = http_code
        self.was_generic = was_generic
        
        super().__init__(self._errors())

    def _errors(self):
        if self.http_code:
            http_error: dict = {
                404: "Not found",
                302: "Moved temporarily, or blocked by captcha",
                403: "Forbidden,or unvalid",
                429: "Too many request",
                500: "Server error",
            }

            return http_error.get(self.http_code, f"Unknown error, please report to the project maintainer. HTTP code {self.http_code}")
        elif self.was_generic:
            return self.message
        else:
            return f"Unknown error, please report to the project maintainer. {self.message}"


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

    def ensure_teritory(func):
        async def decor(self, *args, **kwargs):
            if not self.teritory:
                ip: str = await get_current_ip(session=self.session)
                self.teritory = await get_country_code(session=self.session, ip=ip)

            return await func(self, *args, **kwargs)
        return decor

    @ensure_teritory
    async def get_tracks(self, query: str) -> list[Track]:
        '''
        Get List of all tracks from database, based by keyword
        '''
        url: str = f"{LYRICSFIND_DOMAIN}api/v1/search"
        params: dict = Param(self.teritory).get_param_search(query=query, limit=self.limit)

        async with self.session.get(url=url, params=params) as resp:
            if resp.status < 400:
                data: dict = await resp.json()

                if data['tracks']:
                    return [Track(x) for x in data['tracks']]
                else:
                    raise LFException(http_code=resp.status)
            else:
                raise LFException(http_code=resp.status)
            
    @ensure_teritory
    async def get_track(self, trackid: str):
        '''
        Get a track from database, specifically by using metadata/trackid.

        e.g If using lfid, makesure pass ```lfid:{track id, without bracket}```\n
        if using apple id do the same ```apple:{track id, without bracket}```\n
        this method apply to other metadata, that specifiaclly refrence into the track.\n
        for reference on metadata, check ```Model``` class.
        '''
        url: str = f"{LYRICSFIND_DOMAIN}api/v1/metadata"
        params: dict = Param(self.teritory).get_param_search(trackid=trackid, limit=self.limit)

        async with self.session.get(url=url, params=params) as resp:
            if resp.status < 400:
                data: dict = await resp.json()

                if data['track']:
                    return Track(data['track'])
                else:
                    raise LFException(http_code=resp.status)
            else:
                raise LFException(http_code=resp.status)

    @ensure_teritory
    async def get_lyrics(self, lfid: str) -> SongData:
        '''
        Get lyric from database, by given track
        '''
        url: str = f"{LYRICSFIND_DOMAIN}api/v1/lyric"
        
        params: dict = Param(self.teritory).get_param_lyrics(lfid=lfid)
        async with self.session.get(url=url, params=params) as resp:
            if resp.status < 400:
                data: dict = await resp.json()
                print(data)

                return SongData(data=data['track'])
            else:
                raise LFException(http_code=resp.status)

    @ensure_teritory
    async def get_translation(self, track: Track, lang: str) -> Translation:
        '''
        Get translated lyric from database, by given track and language.

        This also dynamically check, if passed language is exist or not, if doesnt, will throw exception.
        '''
        if not track.available_translations:
            raise LFException(message="No translation found on this track!", was_generic=True)

        url: str = f"{LYRICSFIND_DOMAIN}api/v1/translation"
        lang = lang.lower()
        if not lang in track.available_translations:
            raise LFException(
                message=f"Please check the language you inputted!. Listed language {track.available_translations}(listed on array, select one))", was_generic=True)

        params: dict = Param(self.teritory).get_param_translation(lfid=track.lfid, traslation_language=lang)
        async with self.session.get(url=url, params=params) as resp:
            if resp.status < 400:
                data: dict = await resp.json()
                return Translation(data=data['track'])
            else:
                raise LFException(http_code=resp.status)
