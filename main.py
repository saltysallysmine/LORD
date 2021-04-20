from flask import Flask, render_template, url_for, request
from pprint import pprint
import lord_api
import json

# consts
with open('../keys.json', 'r', encoding='utf-8') as fp:
    secret_data = json.load(fp)
API_KEY = secret_data['api_key']
MAIN_URL = 'https://the-one-api.dev/v2/'

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_data['app_secret_key']


@app.route('/')
def index_page():
    html_keys = {
        'title': 'LORD',
        'css_url': url_for('static', filename='/css/base.css')
    }
    return render_template('index.html', **html_keys)


@app.route('/characters', methods=['GET', 'POST'])
def characters_page():
    html_keys = {
        'title': 'Characters',
        'css_url': url_for('static', filename='/css/characters.css')
    }

    if request.method == 'GET':
        # characters_params
        with open('../characters_params.json', 'r', encoding='utf-8') as fp:
            characters_params = json.load(fp)
        descriptions = {}()
        for key, value in characters_params.items():
            descriptions[key] = value
        html_keys['descriptions'] = descriptions
        return render_template('characters.html', **html_keys)

    if request.method == 'POST':
        pprint(request.form)
        return render_template('characters.html', **html_keys)

if __name__ == "__main__":
    app.run()
    lord_api.set_consts({
        'API_KEY': API_KEY,
        'MAIN_URL': MAIN_URL
    })
    # pprint(lord_api.get_character())
