from pydantic import BaseModel, Field


class Artist(BaseModel):
    name: str = Field()
    lfid: str = Field()
    slug: str = Field()
    is_primary: bool = Field()


class Album(BaseModel):
    id: str = Field()
    title: str = Field()
    releaseYear: int = Field()
    coverArt: str = Field()


class Track(BaseModel):
    lfid: str = Field()
    language: str = Field()
    available_translations: list[str] = Field()
    rovi: str = Field()
    gracenote: str = Field()
    apple: int = Field()
    deezer: int = Field()
    isrcs: list[str] = Field()
    instrumental: bool = Field()
    viewable: bool = Field()
    has_lrc: bool = Field()
    has_contentfilter: bool = Field()
    has_emotion: bool = Field()
    has_sentiment: bool = Field()
    lrc_verified: bool = Field()
    title: str = Field()
    artists: list[Artist] = Field()
    artist: str = Field()
    last_update: str = Field()
    snippet: str = Field()
    context: str = Field()
    score: float = Field()
    glp: str = Field()
    slug: str = Field()
    album: Album = Field()


class SongData(Track):
    lyrics: str = Field()
    copyright: str = Field()
    writer: str = Field()


class Lrc(BaseModel):
    lrc_timestamp: str = Field()
    milliseconds: str = Field()
    duration: str = Field()
    line: str = Field()


class Translation(Track):
    translation: str = Field()
    lrc_version: str = Field()
    lrc: list[Lrc] = Field()
    copyright: str = Field()
    writer: str = Field()

class ModelResponse(BaseModel):
    status: int = Field()
    message: str = Field()
    data: str | list[Track] | Track | SongData | Translation | None = Field()

class ModelResponseSearch(BaseModel):
    status: int = Field()
    message: str = Field()
    data: list[Track] | None = Field()

class ModelResponseTrack(BaseModel):
    status: int = Field()
    message: str = Field()
    data: Track | None = Field()

class ModelResponseSongData(BaseModel):
    status: int = Field()
    message: str = Field()
    data: SongData | None = Field()

class ModelResponseTranslation(BaseModel):
    status: int = Field()
    message: str = Field()
    data: Translation | None = Field()