class Track:
    def __init__(self, data: dict) -> None:
        self.origin: dict = data
        self.lfid: str = data.get('lfid', '')
        self.language: str = data.get('language', '')
        self.available_translations: list[str] = data.get(
            'available_translations', [])
        self.rovi: str = data.get('rovi', '')
        self.gracenote: str = data.get('gracenote', '')
        self.apple: int = data.get('apple', 0)
        self.deezer: int = data.get('deezer', 0)
        self.isrcs: list[str] = data.get('isrcs', [])
        self.instrumental: bool = data.get('instrumental', False)
        self.viewable: bool = data.get('viewable', False)
        self.has_lrc: bool = data.get('has_lrc', False)
        self.has_contentfilter: bool = data.get('has_contentfilter', False)
        self.has_emotion: bool = data.get('has_emotion', False)
        self.has_sentiment: bool = data.get('has_sentiment', False)
        self.lrc_verified: bool = data.get('lrc_verified', False)
        self.title: str = data.get('title', '')
        self.artists: list[Artist] = [
            Artist(x) for x in data.get('artists', [])]
        self.artist: str = data.get('artist', {}).get('name', '')
        self.last_update: str = data.get('last_update', '')
        self.snippet: str = data.get('snippet', '')
        self.context: str = data.get('context', '')
        self.score: float = data.get('score', 0.0)
        self.glp: str = data.get('glp', '')
        self.slug: str = data.get('slug', '')
        self.album: Album = Album(data.get('album', {}))

    def __repr__(self) -> str:
        return f'''<Track(name={repr(self.title)}, artist={repr(" and ".join(x.name for x in self.artists))})>'''


class Artist:
    def __init__(self, data: dict) -> None:
        self.name: str = data.get('name', '')
        self.lfid: str = data.get('lfid', '')
        self.slug: str = data.get('slug', '')
        self.is_primary: bool = data.get('is_primary', False)

    def __repr__(self) -> str:
        return f'''<Artist(name={repr(self.name)}, slug={repr(self.slug)})>'''


class Album:
    def __init__(self, data: dict) -> None:
        self.id: str = data.get('id', '')
        self.title: str = data.get('title', '')
        self.releaseYear: int = data.get('releaseYear', 0)
        self.coverArt: str = f"http://images.lyricfind.com/images/{
            data.get('coverArt', '')}"

    def __repr__(self) -> str:
        return f'''<Album(title={repr(self.title)}, releaseYear={repr(self.releaseYear)})>'''


class SongData(Track):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.lyrics: str = data.get('lyrics', '')
        self.copyright: str = data.get('copyright', '')
        self.writer: str = data.get('writer', '')


class Translation(Track):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.translation: str = data.get('translation', '')
        self.lrc_version: str = data.get('lrc_version', '')
        self.lrc: list[Lrc] = [Lrc(x) for x in data.get('lrc', [])]
        self.copyright: str = data.get('copyright', '')
        self.writer: str = data.get('writer', '')


class Lrc:
    def __init__(self, data: dict) -> None:
        self.lrc_timestamp: str = data.get('lrc_timestamp', '')
        self.milliseconds: str = data.get('milliseconds', '')
        self.duration: str = data.get('duration', '')
        self.line: str = data.get('line', '')

    def __repr__(self) -> str:
        return f'''<LRC(timestamp={repr(self.lrc_timestamp)}, line={repr(self.line)})>'''
