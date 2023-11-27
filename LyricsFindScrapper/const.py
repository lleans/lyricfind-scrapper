LYRICSFIND_DOMAIN = "https://lyrics.lyricfind.com/"

IP_LOCATION_API = "https://api.iplocation.net/"


def get_param_search(query: str, limit: int, teritory: str):
    return {
        'reqtype': 'default',
        'territory': teritory,
        'searchtype': 'track',
        'limit': limit,
        'all': query,
        'alltracks': 'no',
        'output': 'json'
    }


def get_param_translation(trackid: str, teritory: str, traslation_language: str):
    return {
        'reqtype': 'default',
        'trackid': f'lfid:{trackid}',
        'territory': teritory,
        'output': 'json',
        'translationlanguage': traslation_language
    }
