from os import environ
from typing import Annotated
from contextlib import asynccontextmanager

from aiohttp import ClientSession

from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

import uvicorn

from LyricsFindScrapper import Search, get_country_code, Track, Translation, LFException, SongData
from model_router import ModelResponse, ModelResponseSearch, ModelResponseTrack, ModelResponseSongData, ModelResponseTranslation


@asynccontextmanager
async def lifespan(_):
    redis = aioredis.from_url("redis://redis")
    FastAPICache.init(RedisBackend(redis), prefix="lyricfind-cache")
    yield

description: str = """
# Lyric Find Scrapper 🎹

LyricsFind is free online lyrics database, using simple scrapper PyQuery and Aiohttp to grab lyrics from the free-website.

## Data Model 📅

All data model, you can see below the docs
"""

app = FastAPI(title='LyricFind Scrapper',
              lifespan=lifespan,
              version="2.0",
              description=description,
              summary="Simple API scrapper on LyricFInd 🎹",
              license_info={
                  "name": "MIT License",
                  "url": "https://github.com/lleans/lyricfind-scrapper/raw/main/LICENSE",
              })


@app.get('/search', responses={
    200: {'description': "Will return data as model below", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      "status": 200,
                      "message": "OK",
                      "data": [
                          {
                              "lfid": "002-1537029",
                              "language": "en",
                              "available_translations": [
                                  "de",
                                  "pt",
                                  "ja",
                                  "it",
                                  "fr",
                                  "es"
                              ],
                              "rovi": "MT0056718073",
                              "gracenote": "GN20XPWNKW2W0WX",
                              "apple": 1452955723,
                              "deezer": 675315012,
                              "isrcs": [
                                  "NL6VJ2311181",
                                  "QZG4T1900008"
                              ],
                              "instrumental": False,
                              "viewable": True,
                              "has_lrc": True,
                              "has_contentfilter": False,
                              "has_emotion": True,
                              "has_sentiment": True,
                              "lrc_verified": True,
                              "title": "Heart To Heart",
                              "artists": [
                                  {
                                      "name": "Mac DeMarco",
                                      "lfid": "lf:115467",
                                      "slug": "mac-demarco",
                                      "is_primary": True
                                  }
                              ],
                              "artist": "Mac DeMarco",
                              "last_update": "2023-04-04 16:02:19",
                              "snippet": "To all the days we were together\r\nTo all the time we were apart\r\nOf each other's lives\r\nHeart to heart\r\nAnd so I had a late arrival\r\nSo we never saw t...",
                              "context": "To all the days we were together\r\nTo all the time we were apart\r\nOf each other's lives\r\n<em>Heart</em> to <em>heart</em>\r\nAnd so I had a late arrival\r\nSo we never saw",
                              "score": 12.249302,
                              "glp": "",
                              "slug": "mac-demarco-heart-to-heart",
                              "album": {
                                  "id": "ms:1611869",
                                  "title": "Here Comes the Cowboy",
                                  "releaseYear": 2019,
                                  "coverArt": "http://images.lyricfind.com/images/cover_art/curation/original/4/c/f/5/6572-aad6-40b5-810c-e1aeb77ff35b.jpg"
                              }
                          },
                          "..."
                      ]
                  }
              }
          }},
    404: {'description': "Will return when data is not found", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 404,
                      'message': "Query not found",
                      'data': "null"
                  }
              }
          }},
    400: {'description': "Will return when peforming bad request", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 400,
                      'message': "Bad request, please check your datatypes or make sure to fill all parameter",
                      'data': "null"
                  }
              }
          }},
    422: {'description': "Will return when peforming bad request", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 400,
                      'message': "Bad request, please check your datatypes or make sure to fill all parameter",
                      'data': "null"
                  }
              }
          }}
})
@cache(expire=86400)
async def search(query: Annotated[str, Query(title="Track keyword", description="Pass your track keyword into here")], request: Request) -> JSONResponse:
    '''
    Get List of all tracks from database, based by keyword
    '''
    resp: ModelResponseSearch = ModelResponseSearch(
        status=200, message="OK", data=None)

    if query:
        async with ClientSession() as sess:
            ip: str = request.client.host

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            query = query.strip()

            data: list[Track] = await api.get_tracks(query=query)
            if len(data) > 0:
                resp.data = data
            else:
                resp.status = 404
                resp.message = "Query not found"

    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.get('/track', responses={
    200: {'description': "Will return data as model below", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      "status": 200,
                      "message": "OK",
                      "data": {
                          "lfid": "002-1537029",
                          "language": "en",
                          "available_translations": [
                              "de",
                              "pt",
                              "ja",
                              "it",
                              "fr",
                              "es"
                          ],
                          "rovi": "MT0056718073",
                          "gracenote": "GN20XPWNKW2W0WX",
                          "apple": 1452955723,
                          "deezer": 675315012,
                          "isrcs": [
                              "NL6VJ2311181",
                              "QZG4T1900008"
                          ],
                          "instrumental": False,
                          "viewable": True,
                          "has_lrc": True,
                          "has_contentfilter": False,
                          "has_emotion": True,
                          "has_sentiment": True,
                          "lrc_verified": True,
                          "title": "Heart To Heart",
                          "artists": [
                              {
                                  "name": "Mac DeMarco",
                                  "lfid": "lf:115467",
                                  "slug": "mac-demarco",
                                  "is_primary": True
                              }
                          ],
                          "artist": "Mac DeMarco",
                          "last_update": "2023-04-04 16:02:19",
                          "snippet": "To all the days we were together\r\nTo all the time we were apart\r\nOf each other's lives\r\nHeart to heart\r\nAnd so I had a late arrival\r\nSo we never saw t...",
                          "context": "",
                          "score": 0,
                          "glp": "",
                          "slug": "mac-demarco-heart-to-heart",
                          "album": {
                              "id": "ms:1611869",
                              "title": "Here Comes the Cowboy",
                              "releaseYear": 2019,
                              "coverArt": "http://images.lyricfind.com/images/cover_art/curation/original/4/c/f/5/6572-aad6-40b5-810c-e1aeb77ff35b.jpg"
                          }
                      }
                  }
              }
          }},
    404: {'description': "Will return when data is not found", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 404,
                      'message': "Query not found",
                      'data': "null"
                  }
              }
          }},
    400: {'description': "Will return when peforming bad request", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 400,
                      'message': "Bad request, please check your datatypes or make sure to fill all parameter",
                      'data': "null"
                  }
              }
          }},
    422: {'description': "Will return when peforming bad request", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 400,
                      'message': "Bad request, please check your datatypes or make sure to fill all parameter",
                      'data': "null"
                  }
              }
          }}
})
@cache(expire=86400)
async def track(trackid: Annotated[str, Query(title="Track id", description="Pass your track id into here")], request: Request) -> JSONResponse:
    '''
    Get a track from database, specifically by using metadata/trackid.

    e.g If using lfid, makesure pass ```lfid:{track id, without bracket}```\n
    if using apple id do the same ```apple:{track id, without bracket}```\n
    this method apply to other metadata, that specifiaclly refrence into the track.\n
    for reference on metadata, check ```Model``` class.
    '''
    resp: ModelResponseTrack = ModelResponseTrack(
        status=200, message="OK", data=None)

    if trackid:
        async with ClientSession() as sess:
            ip: str = request.client.host

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            trackid = trackid.strip()

            data: Track = await api.get_track(trackid=trackid)
            if data:
                resp.data = data
            else:
                resp.status = 404
                resp.message = "Track not found"

    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.get('/lyric', responses={
    200: {'description': "Will return data as model below", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      "status": 200,
                      "message": "OK",
                      "data": {
                          "lfid": "002-1537029",
                          "language": "en",
                          "available_translations": [
                              "de",
                              "pt",
                              "ja",
                              "it",
                              "fr",
                              "es"
                          ],
                          "rovi": "MT0056718073",
                          "gracenote": "GN20XPWNKW2W0WX",
                          "apple": 1452955723,
                          "deezer": 675315012,
                          "isrcs": [
                              "NL6VJ2311181",
                              "QZG4T1900008"
                          ],
                          "instrumental": False,
                          "viewable": True,
                          "has_lrc": True,
                          "has_contentfilter": False,
                          "has_emotion": True,
                          "has_sentiment": True,
                          "lrc_verified": True,
                          "title": "Heart To Heart",
                          "artists": [
                              {
                                  "name": "Mac DeMarco",
                                  "lfid": "lf:115467",
                                  "slug": "mac-demarco",
                                  "is_primary": True
                              }
                          ],
                          "artist": "Mac DeMarco",
                          "last_update": "2023-04-04 16:02:19",
                          "snippet": "",
                          "context": "",
                          "score": 0,
                          "glp": "",
                          "slug": "mac-demarco-heart-to-heart",
                          "album": {
                              "id": "ms:1611869",
                              "title": "Here Comes the Cowboy",
                              "releaseYear": 2019,
                              "coverArt": "http://images.lyricfind.com/images/cover_art/curation/original/4/c/f/5/6572-aad6-40b5-810c-e1aeb77ff35b.jpg"
                          },
                          "lyrics": "To all the days we were together\nTo all the time we were apart\nOf each other's lives\nHeart to heart\nAnd so I had a late arrival\nSo we never saw the start\nOf each other's lives\nHeart to heart\n\nHeart to heart\nHeart to heart\nHeart to heart\nHeart to heart\n\nKnow it seems so quick and easy\nSentimentally assumed\nWalking parallels\nHeart to heart\nTo all the days we were together\nTo all the time we played a part\nIn each other's lives\nHeart to heart\n\nHeart to heart\nHeart to heart\nHeart to heart\nHeart to heart\nHeart to heart\nHeart to heart\nHeart to heart\nHeart to heart",
                          "copyright": "Lyrics © Kobalt Music Publishing Ltd.",
                          "writer": "MacBriare DeMarco"
                      }
                  }
              }
          }},
    404: {'description': "Will return when data is not found", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 404,
                      'message': "Query not found",
                      'data': "null"
                  }
              }
          }},
    400: {'description': "Will return when peforming bad request", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 400,
                      'message': "Bad request, please check your datatypes or make sure to fill all parameter",
                      'data': "null"
                  }
              }
          }},
    422: {'description': "Will return when peforming bad request", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 400,
                      'message': "Bad request, please check your datatypes or make sure to fill all parameter",
                      'data': "null"
                  }
              }
          }}
})
@cache(expire=86400)
async def lyric(lfid: Annotated[str, Query(title="Lfid", description="Pass your lfid into here(get it from the request before ```/track``` and ```/search```)")], request: Request) -> JSONResponse:
    '''
    Get lyric from database, by given track
    '''
    resp: ModelResponseSongData = ModelResponseSongData(
        status=200, message="OK", data=None)

    if lfid:
        async with ClientSession() as sess:
            ip: str = request.client.host

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            lfid = lfid.strip()

            data: SongData = await api.get_lyrics(lfid=lfid)
            if data:
                resp.data = data
            else:
                resp.status = 404
                resp.message = "Lyric not found"

    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.get('/translation', responses={
    200: {'description': "Will return data as model below", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      "status": 200,
                      "message": "OK",
                      "data": {
                          "lfid": "002-1537029",
                          "language": "",
                          "available_translations": [
                              "de",
                              "pt",
                              "ja",
                              "it",
                              "fr",
                              "es"
                          ],
                          "rovi": "MT0056718073",
                          "gracenote": "GN20XPWNKW2W0WX",
                          "apple": 1452955723,
                          "deezer": 675315012,
                          "isrcs": [
                              "NL6VJ2311181",
                              "QZG4T1900008"
                          ],
                          "instrumental": False,
                          "viewable": True,
                          "has_lrc": True,
                          "has_contentfilter": False,
                          "has_emotion": True,
                          "has_sentiment": True,
                          "lrc_verified": True,
                          "title": "Heart To Heart",
                          "artists": [
                              {
                                  "name": "Mac DeMarco",
                                  "lfid": "lf:115467",
                                  "slug": "mac-demarco",
                                  "is_primary": True
                              }
                          ],
                          "artist": "Mac DeMarco",
                          "last_update": "2023-04-04 16:02:19",
                          "snippet": "",
                          "context": "",
                          "score": 0,
                          "glp": "",
                          "slug": "mac-demarco-heart-to-heart",
                          "album": {
                              "id": "ms:1611869",
                              "title": "Here Comes the Cowboy",
                              "releaseYear": 2019,
                              "coverArt": "http://images.lyricfind.com/images/cover_art/curation/original/4/c/f/5/6572-aad6-40b5-810c-e1aeb77ff35b.jpg"
                          },
                          "translation": "Auf all die Tage, an denen wir zusammen waren\nAuf all die Zeit, die wir getrennt waren\nAn das Leben des anderen\nVon Herz zu Herz\nUnd so hatte ich eine späte Ankunft\nSo sahen wir nie den Anfang\nDes Lebens des anderen\nVon Herz zu Herz\n\nVon Herz zu Herz\nVon Herz zu Herz\nVon Herz zu Herz\nVon Herz zu Herz\n\nIch weiß, es scheint so schnell und einfach\nGefühlsmäßig angenommen\nParallelen gehen\nVon Herz zu Herz\nZu all den Tagen, die wir zusammen waren\nZu all der Zeit, die wir getrennt spielten\nIm Leben des anderen\nVon Herz zu Herz\n\nVon Herz zu Herz\nVon Herz zu Herz\nVon Herz zu Herz\nVon Herz zu Herz\nVon Herz zu Herz\nVon Herz zu Herz\nVon Herz zu Herz\nVon Herz zu Herz",
                          "lrc_version": "1.1",
                          "lrc": [
                              {
                                  "lrc_timestamp": "[00:24.80]",
                                  "milliseconds": "24800",
                                  "duration": "3350",
                                  "line": "Auf all die Tage, an denen wir zusammen waren"
                              },
                              {
                                  "lrc_timestamp": "[00:31.15]",
                                  "milliseconds": "31150",
                                  "duration": "3010",
                                  "line": "Auf all die Zeit, die wir getrennt waren"
                              },
                              {
                                  "lrc_timestamp": "[00:37.71]",
                                  "milliseconds": "37710",
                                  "duration": "2330",
                                  "line": "An das Leben des anderen"
                              },
                              {
                                  "lrc_timestamp": "[00:44.14]",
                                  "milliseconds": "44140",
                                  "duration": "1610",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[00:50.35]",
                                  "milliseconds": "50350",
                                  "duration": "3360",
                                  "line": "Und so hatte ich eine späte Ankunft"
                              },
                              {
                                  "lrc_timestamp": "[00:56.91]",
                                  "milliseconds": "56910",
                                  "duration": "3250",
                                  "line": "So sahen wir nie den Anfang"
                              },
                              {
                                  "lrc_timestamp": "[01:03.36]",
                                  "milliseconds": "63360",
                                  "duration": "2420",
                                  "line": "Des Lebens des anderen"
                              },
                              {
                                  "lrc_timestamp": "[01:09.73]",
                                  "milliseconds": "69730",
                                  "duration": "1630",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "",
                                  "milliseconds": "",
                                  "duration": "",
                                  "line": ""
                              },
                              {
                                  "lrc_timestamp": "[01:16.16]",
                                  "milliseconds": "76160",
                                  "duration": "1630",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[01:22.54]",
                                  "milliseconds": "82540",
                                  "duration": "1650",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[01:28.94]",
                                  "milliseconds": "88940",
                                  "duration": "1620",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[01:35.36]",
                                  "milliseconds": "95360",
                                  "duration": "1620",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "",
                                  "milliseconds": "",
                                  "duration": "",
                                  "line": ""
                              },
                              {
                                  "lrc_timestamp": "[01:41.73]",
                                  "milliseconds": "101730",
                                  "duration": "3230",
                                  "line": "Ich weiß, es scheint so schnell und einfach"
                              },
                              {
                                  "lrc_timestamp": "[01:48.11]",
                                  "milliseconds": "108110",
                                  "duration": "2830",
                                  "line": "Gefühlsmäßig angenommen"
                              },
                              {
                                  "lrc_timestamp": "[01:54.54]",
                                  "milliseconds": "114540",
                                  "duration": "2020",
                                  "line": "Parallelen gehen"
                              },
                              {
                                  "lrc_timestamp": "[02:00.91]",
                                  "milliseconds": "120910",
                                  "duration": "1620",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[02:07.13]",
                                  "milliseconds": "127130",
                                  "duration": "3410",
                                  "line": "Zu all den Tagen, die wir zusammen waren"
                              },
                              {
                                  "lrc_timestamp": "[02:13.54]",
                                  "milliseconds": "133540",
                                  "duration": "3430",
                                  "line": "Zu all der Zeit, die wir getrennt spielten"
                              },
                              {
                                  "lrc_timestamp": "[02:20.12]",
                                  "milliseconds": "140120",
                                  "duration": "2440",
                                  "line": "Im Leben des anderen"
                              },
                              {
                                  "lrc_timestamp": "[02:26.56]",
                                  "milliseconds": "146560",
                                  "duration": "1580",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "",
                                  "milliseconds": "",
                                  "duration": "",
                                  "line": ""
                              },
                              {
                                  "lrc_timestamp": "[02:32.94]",
                                  "milliseconds": "152940",
                                  "duration": "1640",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[02:39.33]",
                                  "milliseconds": "159330",
                                  "duration": "1600",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[02:45.73]",
                                  "milliseconds": "165730",
                                  "duration": "1610",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[02:52.14]",
                                  "milliseconds": "172140",
                                  "duration": "1640",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[02:58.53]",
                                  "milliseconds": "178530",
                                  "duration": "1640",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[03:04.92]",
                                  "milliseconds": "184920",
                                  "duration": "1620",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[03:11.34]",
                                  "milliseconds": "191340",
                                  "duration": "1620",
                                  "line": "Von Herz zu Herz"
                              },
                              {
                                  "lrc_timestamp": "[03:17.73]",
                                  "milliseconds": "197730",
                                  "duration": "1620",
                                  "line": "Von Herz zu Herz"
                              }
                          ],
                          "copyright": "Lyrics © Kobalt Music Publishing Ltd.",
                          "writer": "MacBriare DeMarco"
                      }
                  }
              }
          }},
    404: {'description': "Will return when data is not found", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 404,
                      'message': "Query not found",
                      'data': "null"
                  }
              }
          }},
    400: {'description': "Will return when peforming bad request", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 400,
                      'message': "Bad request, please check your datatypes or make sure to fill all parameter",
                      'data': "null"
                  }
              }
          }},
    422: {'description': "Will return when peforming bad request", 'model': ModelResponse,
          'content': {
              'application/json': {
                  'example': {
                      'status': 400,
                      'message': "Bad request, please check your datatypes or make sure to fill all parameter",
                      'data': "null"
                  }
              }
          }}
})
@cache(expire=86400)
async def translation(lfid: Annotated[str, Query(title="Lfid", description="Pass your lfid into here(get it from the request before ```/track``` and ```/search``` and ```/lyric```)")],
                      lang: Annotated[str, Query(title="Selected language", description="Pass your target language to translate(make sure the target language exist in track data)")] = 'en', *, request: Request):
    '''
    Get translated lyric from database, by given track and language.

    This also dynamically check, if passed language is exist or not, if doesnt, will throw exception.
    '''
    resp: ModelResponseTranslation = ModelResponseTranslation(
        status=200, message="OK", data=None)

    if lfid:
        async with ClientSession() as sess:
            ip: str = request.client.host

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            lfid = lfid.strip()

            track: Track = await api.get_track(trackid=f'lfid:{lfid}')
            data: Translation = await api.get_translation(track=track, lang=lang)
            if data:
                resp.data = data
            else:
                resp.status = 404
                resp.message = "Translation not found"

    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.exception_handler(404)
async def error_handling_lf(_, __) -> RedirectResponse:
    return RedirectResponse(url='/docs')


@app.exception_handler(RequestValidationError)
async def validation_handling(_, __) -> JSONResponse:
    resp: ModelResponse = ModelResponse(
        status=400, message="Bad request, please check your datatypes or make sure to fill all parameter", data=None)
    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)


@app.exception_handler(500)
@app.exception_handler(LFException)
async def error_handling(_, exec: Exception) -> JSONResponse:
    resp: ModelResponse = ModelResponse(
        status=500, message="Something went wrong!! " + str(exec), data=None)

    if isinstance(exec, LFException):
        resp.status = exec.http_code or 500
        resp.message = exec.message or str(exec)

    return JSONResponse(content=jsonable_encoder(resp), status_code=resp.status)

if __name__ == "__main__":
    uvicorn.run("router:app", host="0.0.0.0",
                port=int(environ.get('PORT')) or 8000, log_level="info", forwarded_allow_ips="*")
