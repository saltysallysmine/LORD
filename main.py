from flask import Flask, render_template, url_for, request, redirect
from pprint import pprint
import google_search_api
from google_search_api import GoogleSearcher
import lord_api
import json
import logging

# logging
logging.basicConfig(filename='lord_logging.log', level=logging.INFO)

# consts
with open('../keys.json', 'r', encoding='utf-8') as fp:
    secret_data = json.load(fp)
LORD_API_KEY = secret_data['lord_api_key']
GOOGLE_API_KEY = secret_data['google_api_key']
CX = secret_data['cx']

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_data['app_secret_key']


@app.route('/')
def index_page():
    html_keys = {
        'title': 'LORD',
        'css_url': url_for('static', filename='/css/base.css')
    }
    logging.info('get index')
    return render_template('index.html', **html_keys)


@app.route('/error')
def error_page():
    html_keys = {
        'title': 'Error',
        'css_url': url_for('static', filename='/css/characters.css'),
        'message': "Something go wrong! We`re trying to fix your problem. Check the desired page after."
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
        logging.info('get characters page')
        return render_template('characters.html', **html_keys)

    if request.method == 'POST':
        try:
            d = {}
            for key, value in request.form.items():
                if value:
                    d[key] = value
            html_keys['characters_list'] = lord_api.get_character(d)['docs']
            logging.info('post characters page')
            # pprint(html_keys)
        except Exception as e:
            logging.error('characters page: ' + str(e))
            redirect('/error')
        return render_template('characters.html', **html_keys)


@app.route('/books')
def books():
    html_keys = {
        'title': 'Books',
        'css_url': url_for('static', filename='/css/books.css')
    }
    logging.info('get books page')
    return render_template('books.html', **html_keys)


@app.route('/movies')
def movies():
    html_keys = {
        'title': 'movies',
        'css_url': url_for('static', filename='/css/movies.css'),
        'movies_list': lord_api.get_movies()['docs']
    }
    if html_keys['movies_list'] is None:
        redirect('/error')
    src_base = '../static/img/movies_poster/'
    posters_src_list = []
    wiki_url_list = []
    wiki_snippet_list = []
    found_results_from_google = GoogleSearcher()
    try:
        for movie in html_keys['movies_list']:
            cur_name = movie['name'].rstrip()
            # way to posters images
            posters_src_list.append(src_base + cur_name + '.jpg')
            # found film info in google
            found_results_from_google.search_for(f'movie {cur_name}')
            wiki_url_list.append(found_results_from_google.get_url())
            # snippet
            cur_snippet = str(found_results_from_google.get_snippet()) \
                .replace('<b>', '') \
                .replace('</b>', '') \
                .replace('<br>', '') \
                .replace('&nbsp;', '')
            wiki_snippet_list.append(cur_snippet)
        html_keys['posters_src_list'] = posters_src_list
        html_keys['wiki_url_list'] = wiki_url_list
        html_keys['wiki_snippet_list'] = wiki_snippet_list

        # pprint(wiki_url_list)
        # pprint(wiki_snippet_list)

        logging.info('get movies page')
        return render_template('movies.html', **html_keys)
    # error
    except Exception as e:
        logging.error('movies page: ' + str(e))
        redirect('/error')


if __name__ == "__main__":
    lord_api.set_consts({
        'LORD_API_KEY': LORD_API_KEY,
    })
    google_search_api.set_consts({
        'GOOGLE_API_KEY': GOOGLE_API_KEY,
        'CX': CX
    })
    # pprint(lord_api.get_character())
    # pprint(lord_api.get_books())
    # pprint(lord_api.get_movies()['docs'][0])
    app.run()
