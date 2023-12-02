LYRICSFIND_DOMAIN = "https://lyrics.lyricfind.com/"

IP_LOCATION_API = "https://api.iplocation.net/"


class Param:

    def __init__(self, teritory: str) -> None:
        self.default_param = {
            'reqtype': 'default',
            'territory': teritory,
            'output': 'json'
        }

    def get_param_search(self, query: str = None, trackid: str = None, *, limit: int):
        temp: dict = self.default_param
        if query:
            temp.update({
                'searchtype': 'track',
                'limit': limit,
                'all': query,
                'alltracks': 'no',
            })
        else:
            temp.update({
                'reqtype': 'metadata',
                'trackid': trackid
            })

        return temp

    def get_param_lyrics(self, lfid: str):
        temp: dict = self.default_param
        temp.update({
            'trackid': f'lfid:{lfid}'
        })
        
        return temp

    def get_param_translation(self, lfid: str, traslation_language: str):
        temp: dict = self.default_param
        temp.update({
            'trackid': f'lfid:{lfid}',
            'translationlanguage': traslation_language
        })

        return temp
