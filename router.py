from os import environ

from contextlib import asynccontextmanager

from aiohttp import ClientSession

from pydantic import BaseModel, Field

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

import uvicorn

from LyricsFindScrapper import Search, get_country_code, Track, Translation, LFException, SongData


@asynccontextmanager
async def lifespan(_):
    redis = aioredis.from_url("redis://redis")
    FastAPICache.init(RedisBackend(redis), prefix="lyricfind-cache")
    yield

app = FastAPI(title='LyricFind Scrapper', lifespan=lifespan, version="2.0")


class ModelResponse(BaseModel):
    status: int
    message: str
    data: dict | list[dict]


@app.get('/search', response_model=ModelResponse, responses={
    200: {'description': "Will return data as model below", 'model': ModelResponse},
    404: {'description': "Will return when data is not found", 'model': ModelResponse},
    422: {'description': "Will return when peforming bad request", 'model': ModelResponse}
})
@cache(expire=86400)
async def search(query: str, request: Request) -> JSONResponse:
    '''
    Get List of all tracks from database, based by keyword
    '''
    resp: ModelResponse = ModelResponse()
    resp.status = 200
    resp.message = "OK"

    if query:
        async with ClientSession() as sess:
            ip: str = request.client.host

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            query = query.strip()

            data: list[Track] = await api.get_tracks(query=query)
            if len(data) > 0:
                resp.data = [x.to_dict() for x in data]
            else:
                resp.status = 404
                resp.message = "Query not found"

    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.get('/track', response_model=ModelResponse, responses={
    200: {'description': "Will return data as model below", 'model': ModelResponse},
    404: {'description': "Will return when data is not found", 'model': ModelResponse},
    422: {'description': "Will return when peforming bad request", 'model': ModelResponse}
})
@cache(expire=86400)
async def track(trackid: str, request: Request) -> JSONResponse:
    '''
    Get a track from database, specifically by using metadata/trackid.

    e.g If using lfid, makesure pass ```lfid:{track id, without bracket}```\n
    if using apple id do the same ```apple:{track id, without bracket}```\n
    this method apply to other metadata, that specifiaclly refrence into the track.\n
    for reference on metadata, check ```Model``` class.
    '''
    resp: ModelResponse = ModelResponse()
    resp.status = 200
    resp.message = "OK"

    if trackid:
        async with ClientSession() as sess:
            ip: str = request.client.host

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            trackid = trackid.strip()

            data: Track = await api.get_track(trackid=trackid)
            if data:
                resp.data = data.to_dict()
            else:
                resp.status = 404
                resp.message = "Track not found"

    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.get('/lyric', response_model=ModelResponse, responses={
    200: {'description': "Will return data as model below", 'model': ModelResponse},
    404: {'description': "Will return when data is not found", 'model': ModelResponse},
    422: {'description': "Will return when peforming bad request", 'model': ModelResponse}
})
@cache(expire=86400)
async def lyric(lfid: str, request: Request) -> JSONResponse:
    '''
    Get lyric from database, by given track
    '''
    resp: ModelResponse = ModelResponse()
    resp.status = 200
    resp.message = "OK"

    if lfid:
        async with ClientSession() as sess:
            ip: str = request.client.host

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            lfid = lfid.strip()

            data: SongData = await api.get_lyrics(lfid=lfid)
            if data:
                resp.data = data.to_dict()
            else:
                resp.status = 404
                resp.message = "Lyric not found"

    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.get('/translation', response_model=ModelResponse, responses={
    200: {'description': "Will return data as model below", 'model': ModelResponse},
    404: {'description': "Will return when data is not found", 'model': ModelResponse},
    422: {'description': "Will return when peforming bad request", 'model': ModelResponse}
})
@cache(expire=86400)
async def translation(lfid: str, lang: str = 'en', *, request: Request):
    '''
    Get translated lyric from database, by given track and language.

    This also dynamically check, if passed language is exist or not, if doesnt, will throw exception.
    '''
    resp: ModelResponse = ModelResponse()
    resp.status = 200
    resp.message = "OK"

    if lfid:
        async with ClientSession() as sess:
            ip: str = request.client.host

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            lfid = lfid.strip()

            track: Track = await api.get_track(trackid=f'lfid:{lfid}')
            data: Translation = await api.get_translation(track=track, lang=lang)
            if data:
                resp.data = data.to_dict()
            else:
                resp.status = 404
                resp.message = "Translation not found"

    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.exception_handler(404)
async def error_handling_lf(_, exec: Exception) -> JSONResponse | RedirectResponse:
    if isinstance(exec, LFException):
        resp: ModelResponse = ModelResponse()
        resp.status = exec.http_code
        resp.message = exec.message
        return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)

    return RedirectResponse(url='/docs')


@app.exception_handler(RequestValidationError)
async def validation_handling(_, __) -> JSONResponse:
    resp: ModelResponse = ModelResponse()
    resp.status = 400
    resp.message = "Bad request, please check your datatypes or make sure to fill all parameter"
    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.exception_handler(500)
async def error_handling(_, exec: Exception) -> JSONResponse:
    resp: ModelResponse = ModelResponse()
    resp.status = 500
    resp.message = "Something went wrong!! " + str(exec)
    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)

if __name__ == "__main__":
    uvicorn.run("router:app", host="0.0.0.0",
                port=int(environ.get('PORT')) or 8000, log_level="info", workers=3, forwarded_allow_ips="*")
