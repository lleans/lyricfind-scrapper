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
async def tracks(query: str = None):
    response: dict = {
        'status': 400,
        'message': 'Bad request',
        'data': ''
    }

    query: str = request.args.get('query') or None

    if query is not None:
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
                        'message': "Query not found"
                    })
            except LFException as e:
                response.update({
                    'message': e.message,
                    'status': e.http_code
                })
            except Exception as ex:
                response.update({
                    'message': f'Something went wrong, {ex}',
                    'status': 500
                })

            sess.close()

    return jsonify(response)


@app.route('/lyrics', methods=['GET'])
@cache.cached(query_string=True)
async def lyrics():
    response: dict = {
        'status': 400,
        'message': 'Bad request',
        'data': ''
    }

    query: str = request.args.get('query') or None

    if query is not None:
        async with ClientSession() as sess:
            list_ip: list[str] = request.headers['x-forwarded-for'].split(',')
            ip: str = list_ip[len(list_ip)-1] or request.remote_addr
            
            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            try:
                query = query.strip()

                tracks: list[Track] = await api.get_tracks(query=query)
                data: SongData = await api.get_lyrics(track=tracks[0])
                if data:
                    response.update({
                        'data': data.to_dict(),
                        'status': 200,
                        'message': "OK"
                    })
                else:
                    response.update({
                        'status': 404,
                        'message': "Query not found"
                    })
            except LFException as e:
                response.update({
                    'message': e.message,
                    'status': e.http_code
                })
            except Exception as ex:
                response.update({
                    'message': f'Something went wrong, {ex}',
                    'status': 500
                })

            sess.close()

    return jsonify(response)


@app.route('/translation', methods=['GET'])
@cache.cached(query_string=True)
async def translation():
    response: dict = {
        'status': 400,
        'message': 'Bad request',
        'data': ''
    }

    query: str = request.args.get('query') or None
    lang: str = request.args.get('lang') or 'en'

    if query is not None:
        async with ClientSession() as sess:
            list_ip: list[str] = request.headers['x-forwarded-for'].split(',')
            ip: str = list_ip[len(list_ip)-1] or request.remote_addr
            
            country_code: str = await get_country_code(session=sess, ip=ip)
            api: Search = Search(session=sess, teritory=country_code)

            try:
                query = query.strip()

                tracks: list[Track] = await api.get_tracks(query=query)
                track: Track = await api.get_lyrics(track=tracks[0])
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
                        'message': "Query not found"
                    })
            except LFException as e:
                response.update({
                    'message': e.message,
                    'status': e.http_code
                })
            except Exception as ex:
                response.update({
                    'message': f'Something went wrong, {ex}',
                    'status': 500
                })

            sess.close()

    return jsonify(response)


@app.errorhandler(400)
@app.errorhandler(404)
async def docs(e):
    return redirect('https://github.com/lleans/lyricfind-scrapper/tree/flask')

if __name__ == "__main__":
    app.run(port=environ.get('PORT') or 8000,
            host='0.0.0.0', threaded=False, debug=False)
