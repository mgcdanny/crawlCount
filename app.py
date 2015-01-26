from flask import Flask, render_template, request
from flask import jsonify
import requests
import re
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from urllib.parse import urljoin

#######################
#### configuration ####
#######################

app = Flask(__name__)


################
#### helper ####
################


def crawl_main(url):
    words = []
    raw_html = crawl(url)
    if raw_html:
        words.extend(get_words(raw_html))
        relevant_links = get_relevant_links(raw_html, url)
        for link in relevant_links:
            temp_html = crawl(link)
            if temp_html:
                words.extend(get_words(temp_html))
    return words


def get_words(html):
    """Take a string of raw html and return a list of words"""
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.get_text()
    nltk.data.path.append('./nltk_data/')  # set the path
    tokens = nltk.word_tokenize(text)
    text = nltk.Text(tokens)
    nonPunct = re.compile('.*[A-Za-z].*')
    words = [w for w in text if nonPunct.match(w)]
    return words


def get_relevant_links(html, base_url):
    """Take raw html and parse out other links that are like 'faw' or 'about'"""
    link_finder = re.compile('faq|about', re.IGNORECASE)
    relevant_links = []
    for link in BeautifulSoup(html).find_all('a'):
        if link_finder.search(str(link)):
            relevant_links.append(urljoin(base_url, link.get('href')))
    return relevant_links


def crawl(url):
    return requests.get(url).text


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/api/crawl', methods=['POST'])
def get_counts():
    # get url
    data = request.json
    url = data["url"]
    # form URL, id necessary
    if 'http://' not in url[:7]:
        url = 'http://' + url
    words = crawl_main(url)
    word_count = Counter(words)
    return jsonify({'freq': word_count})
 


if __name__ == '__main__':
    app.run(debug=True)




