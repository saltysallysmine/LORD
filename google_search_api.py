import requests
from pprint import pprint

GOOGLE_API_KEY = None
CX = None
MAIN_URL = 'https://www.googleapis.com/customsearch/v1'
params = {}


def set_consts(d: dict):
    global GOOGLE_API_KEY, MAIN_URL, CX, params
    GOOGLE_API_KEY = d['GOOGLE_API_KEY']
    CX = d['CX']
    params = {
        'key': GOOGLE_API_KEY,
        'cx': CX
    }


def search_for(query):
    global MAIN_URL, params
    params['q'] = query
    # ans = requests.get(MAIN_URL, params=params).json()['items'][0]
    # return ans['formattedUrl'], ans['htmlSnippet']
    return requests.get(MAIN_URL, params=params).json()


if __name__ == "__main__":
    pass
