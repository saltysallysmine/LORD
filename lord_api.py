import requests

API_KEY = None
MAIN_URL = None
headers = None


def set_consts(d: dict):
    global API_KEY, MAIN_URL, headers
    API_KEY = d['API_KEY']
    MAIN_URL = d['MAIN_URL']
    headers = {
        'Authorization': "Bearer " + API_KEY
    }


def get_character(params={}):
    return requests.get(MAIN_URL + 'character', headers=headers,
           params=params).json()

if __name__ == "__main__":
    pass
