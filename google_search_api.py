import requests
from pprint import pprint

GOOGLE_API_KEY = None
CX = None
MAIN_URL = 'https://www.googleapis.com/customsearch/v1'
params = {}


class GoogleSearcher:
    def __init__(self):
        self.response = None

    def search_for(self, query):
        global MAIN_URL, params
        params['q'] = query
        # return ans[], ans[']
        try:
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # q = 1 / 0
            # print(0)
            self.response = requests.get(MAIN_URL, params=params).json()['items'][0]
        except Exception:
            print(1)
            self.response = {
                'formattedUrl': f'https://www.google.ru/search?q={query}',
                'htmlSnippet': 'You can try to find information about it on wiki'
            }

    def get_url(self):
        if self.response:
            return self.response.get('formattedUrl', "#")

    def get_snippet(self):
        if self.response:
            return self.response.get('htmlSnippet', '')


def set_consts(d: dict):
    global GOOGLE_API_KEY, MAIN_URL, CX, params
    GOOGLE_API_KEY = d['GOOGLE_API_KEY']
    CX = d['CX']
    params = {
        'key': GOOGLE_API_KEY,
        'cx': CX
    }


def search_for(query) -> dict:
    global MAIN_URL, params
    params['q'] = query
    return requests.get(MAIN_URL, params=params).json()


if __name__ == "__main__":
    pass
