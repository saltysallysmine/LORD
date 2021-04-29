import requests

LORD_API_KEY = None
MAIN_URL = 'https://the-one-api.dev/v2/'
headers = None


def set_consts(d: dict):
    global LORD_API_KEY, MAIN_URL, headers
    LORD_API_KEY = d['LORD_API_KEY']
    headers = {
        'Authorization': "Bearer " + LORD_API_KEY
    }


def get_character(params=None):
    global headers
    if params is None:
        params = {}
    # print(MAIN_URL)
    try:
        return requests.get(MAIN_URL + 'character', headers=headers,
                            params=params).json()
    except Exception:
        # print(e)
        # print(requests.get(MAIN_URL + 'character', headers=headers,
        #              params=params).json())
        return None


def get_books():
    global headers
    try:
        return requests.get(MAIN_URL + 'book', headers=headers).json()
    except Exception:
        return None


def get_movies():
    global headers
    try:
        return requests.get(MAIN_URL + 'movie', headers=headers).json()
    except Exception:
        return None


if __name__ == "__main__":
    # get_character({'gender': 'Males', 'hair': 'Brown (movie)', 'realm': 'Doors of Durin'})
    pass
