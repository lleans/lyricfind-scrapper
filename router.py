from os import environ

from flask import Flask, jsonify, redirect, request
from flask_caching import Cache
from aiohttp import ClientSession
from LyricsFindScrapper import Search, get_country_code, Track, Translation, LFException, SongData

config: dict = {
    'CORS_HEADERS': 'Content-Type',
    'JSON_SORT_KEYS': False,
    'CACHE_TYPE': 'FileSystemCache',
    "CACHE_DEFAULT_TIMEOUT": 86400,
    "CACHE_DIR": "cache"
}

app: Flask = Flask('lyricfind_scrapper')
app.config.from_mapping(config)
cache: Cache = Cache(app)


@app.route('/search', methods=['GET'])
@cache.cached(query_string=True)
async def search():
    response: dict = {
        'status': 400,
        'message': 'Bad request',
        'data': 'need query param as, query:your keyword'
    }

    query: str = request.args.get('query')

    if query:
        async with ClientSession() as sess:
            list_ip: list[str] = request.headers['x-forwarded-for'].split(',')
            ip: str = list_ip[len(list_ip)-1] or request.remote_addr

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            try:
                query = query.strip()

                data: list[Track] = await api.get_tracks(query=query)
                if len(data) > 0:
                    response.update({
                        'data': [x.to_dict() for x in data],
                        'status': 200,
                        'message': "OK"
                    })
                else:
                    response.update({
                        'status': 404,
                        'message': "Query not found",
                        'data': ''
                    })
            except LFException as e:
                response.update({
                    'message': e.message,
                    'status': e.http_code,
                    'data': ''
                })
            except Exception as ex:
                response.update({
                    'message': f'Something went wrong, {ex}',
                    'status': 500,
                    'data': ''
                })

    return jsonify(response), response.get('status', 500)


@app.route('/track', methods=['GET'])
@cache.cached(query_string=True)
async def track():
    response: dict = {
        'status': 400,
        'message': 'Bad request',
        'data': 'need trackid param as, trackid:your trackid(check docs)'
    }

    trackid: str = request.args.get('trackid')

    if trackid:
        async with ClientSession() as sess:
            list_ip: list[str] = request.headers['x-forwarded-for'].split(',')
            ip: str = list_ip[len(list_ip)-1] or request.remote_addr

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            try:
                trackid = trackid.strip()

                data: Track = await api.get_track(trackid=trackid)
                if data:
                    response.update({
                        'data': data.to_dict(),
                        'status': 200,
                        'message': "OK"
                    })
                else:
                    response.update({
                        'status': 404,
                        'message': "Track not found",
                        'data': ''
                    })
            except LFException as e:
                response.update({
                    'message': e.message,
                    'status': e.http_code,
                    'data': ''
                })
            except Exception as ex:
                response.update({
                    'message': f'Something went wrong, {ex}',
                    'status': 500,
                    'data': ''
                })

    return jsonify(response), response.get('status', 500)


@app.route('/lyric', methods=['GET'])
@cache.cached(query_string=True)
async def lyric():
    response: dict = {
        'status': 400,
        'message': 'Bad request',
        'data': 'need lfid param as, lfid:your lfid(check docs)'
    }

    lfid: str = request.args.get('lfid')

    if lfid:
        async with ClientSession() as sess:
            list_ip: list[str] = request.headers['x-forwarded-for'].split(',')
            ip: str = list_ip[len(list_ip)-1] or request.remote_addr

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            try:
                lfid = lfid.strip()

                data: SongData = await api.get_lyrics(lfid=lfid)
                if data:
                    response.update({
                        'data': data.to_dict(),
                        'status': 200,
                        'message': "OK"
                    })
                else:
                    response.update({
                        'status': 404,
                        'message': "Lyric not found",
                        'data': ''
                    })
            except LFException as e:
                response.update({
                    'message': e.message,
                    'status': e.http_code,
                    'data': ''
                })
            except Exception as ex:
                response.update({
                    'message': f'Something went wrong, {ex}',
                    'status': 500,
                    'data': ''
                })

    return jsonify(response), response.get('status', 500)


@app.route('/translation', methods=['GET'])
@cache.cached(query_string=True)
async def translation():
    response: dict = {
        'status': 400,
        'message': 'Bad request',
        'data': 'need lfid, lang param as, lfid:your lfid(check docs), lang: your lang(check docs)'
    }

    lfid: str = request.args.get('lfid')
    lang: str = request.args.get('lang', 'en')

    if lfid:
        async with ClientSession() as sess:
            list_ip: list[str] = request.headers['x-forwarded-for'].split(',')
            ip: str = list_ip[len(list_ip)-1] or request.remote_addr

            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            try:
                lfid = lfid.strip()

                track: Track = await api.get_track(trackid=f'lfid:{lfid}')
                data: Translation = await api.get_translation(track=track, lang=lang)
                if data:
                    response.update({
                        'data': data.to_dict(),
                        'status': 200,
                        'message': "OK"
                    })
                else:
                    response.update({
                        'status': 404,
                        'message': "Translation not found"
                    })
            except LFException as e:
                response.update({
                    'message': e.message,
                    'status': e.http_code,
                    'data': ''
                })
            except Exception as ex:
                response.update({
                    'message': f'Something went wrong, {ex}',
                    'status': 500,
                    'data': ''
                })

    return jsonify(response), response.get('status', 500)


@app.errorhandler(400)
@app.errorhandler(404)
async def docs(e):
    return redirect('https://github.com/lleans/lyricfind-scrapper/tree/flask')

if __name__ == "__main__":
    app.run(port=environ.get('PORT') or 8000,
            host='0.0.0.0', threaded=False, debug=False)
