from flask import Flask, render_template, url_for, request, redirect
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


@app.route('/error')
def error_page():
    html_keys = {
        'title': 'Error',
        'css_url': url_for('static', filename='/css/characters.css'),
        'message': "Something go wrong!"
    }
    return render_template('base.html', **html_keys)


@app.route('/characters', methods=['GET', 'POST'])
def characters_page():
    html_keys = {
        'title': 'Characters',
        'css_url': url_for('static', filename='/css/characters.css')
    }
    # characters_params
    with open('../characters_params.json', 'r', encoding='utf-8') as fp:
        characters_params = json.load(fp)
        descriptions = {}
        for key, value in characters_params.items():
            descriptions[key] = value
            html_keys['descriptions'] = descriptions

    if request.method == 'GET':
        return render_template('characters.html', **html_keys)

    if request.method == 'POST':
        try:
            d = {}
            for key, value in request.form.items():
                if value:
                    d[key] = value
            html_keys['characters_list'] = lord_api.get_character(d)['docs']
            # pprint(html_keys)
        except Exception as e:
            pprint(e)
        return render_template('characters.html', **html_keys)


@app.route('/books')
def books():
    html_keys = {
        'title': 'Books',
        'css_url': url_for('static', filename='/css/books.css')
    }
    return render_template('books.html', **html_keys)


@app.route('/movies')
def movies():
    html_keys = {
        'title': 'movies',
        'css_url': url_for('static', filename='/css/movies.css'),
        'movies_list': lord_api.get_movies()['docs']
    }
    return render_template('movies.html', **html_keys)


if __name__ == "__main__":
    lord_api.set_consts({
        'API_KEY': API_KEY,
        'MAIN_URL': MAIN_URL
    })
    # pprint(lord_api.get_character())
    # pprint(lord_api.get_books())
    # pprint(lord_api.get_movies()['docs'][0])
    app.run()
