import requests
import nltk 
from bs4 import BeautifulSoup
import re
from collections import Counter
from urllib.parse import urljoin
from collections import Counter


"""
#base64 decoder for screen_shot
fh = open("imageToSave.png", "wb")
fh.write(base64.decodestring(bytes(data['screen_shot'], 'UTF-8' )))
fh.close()
"""


def crawl_main(url):
    data = {'url_orig': url, 'current_url': None, 'screen_shot': None, 'html': None, 'word_freq': None}
    words = []
    text = ''
    freq = None
    text, links, data['url_crawl'], data['screen_shot'], data['html'] = crawl(url)
    for link in links:
        more_text, _, _, _, _ = crawl(link)
        if more_text:
            text = text + ' ' + more_text
    words = get_words(text)
    if words:
        data['word_freq'] = Counter(words)
    return data


def get_words(text):
    """Take a string of raw html and return a list of words"""
    nltk.data.path.append('../nltk_data/')  # set the path
    tokens = nltk.word_tokenize(text)
    text = nltk.Text(tokens)
    nonPunct = re.compile('.*[A-Za-z].*')
    words = [w for w in text if nonPunct.match(w)]
    return words


def get_relevant_links(html, base_url):
    """Take raw html and parse out other links that are like 'faw' or 'about'"""
    link_finder = re.compile('faq|about|blog', re.IGNORECASE)
    relevant_links = []
    for link in BeautifulSoup(html).find_all('a'):
        if link_finder.search(str(link)):
            relevant_links.append(urljoin(base_url, link.get('href')))
    return relevant_links


def crawl(url):
    text = ''
    links = []
    link_finder = re.compile('faq|about|blog', re.IGNORECASE)
    domain_not_found = re.compile('.?domain.?not.?found', re.IGNORECASE)
    driver = webdriver.PhantomJS()
    driver.set_window_size(1200,1200)
    driver.get(url)
    if domain_not_found.search(driver.current_url):
        #TODO: perhaps dont' fail so silently... return error message
        return text, links, None, None, None
    text = driver.find_element_by_xpath("//html").text
    for a in driver.find_elements_by_tag_name('a'):
        href = a.get_attribute('href')
        if href:
            if link_finder.search(href):
                links.append(href)
    current_url = driver.current_url
    screen_shot = driver.get_screenshot_as_base64()
    html= driver.page_source
    driver.quit()
    return text, links, current_url, screen_shot, html 
    #return requests.get(url).text

"""
#Old shit, but light weight compared to above
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
    nltk.data.path.append('../nltk_data/')  # set the path
    tokens = nltk.word_tokenize(text)
    text = nltk.Text(tokens)
    nonPunct = re.compile('.*[A-Za-z].*')
    words = [w for w in text if nonPunct.match(w)]
    return words


def get_relevant_links(html, base_url):
    """Take raw html and parse out other links that are like 'faw' or 'about'"""
    link_finder = re.compile('faq|about|blog', re.IGNORECASE)
    relevant_links = []
    for link in BeautifulSoup(html).find_all('a'):
        if link_finder.search(str(link)):
            relevant_links.append(urljoin(base_url, link.get('href')))
    return relevant_links


def crawl(url):
    return requests.get(url).text
"""