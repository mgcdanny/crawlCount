from flask import Flask, render_template, request
from flask import jsonify
import requests
import re
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from urllib.parse import urljoin
from utils.scrape import crawl_main

#######################
#### configuration ####
#######################

app = Flask(__name__)


################
#### helper ####
################


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/api/crawl', methods=['POST'])
def get_counts():
    # get url
    data = request.json
    url = data["url"]
    # form URL, id necessary
    if 'http://' not in url[:7] and 'https://' not in url[:8]:
        url = 'http://' + url
    data = crawl_main(url)
    return jsonify(data)
 

if __name__ == '__main__':
    app.run(debug=True)




