"""
This script will scrape data from all articles published
at http://isbullsh.it (url, author, date, title)
"""

import re
import json
import lxml.html
import requests

# Regex pattern corresponding to all isbullsh.it articles url
# \d{4} corresponds to the release year
# \d{2} corresponds to the release month
# [\w-]+ corresponds to the slug
ARTICLE_URL_PATTERN = r'http://isbullsh\.it/\d{4}/\d{2}/[\w-]+'

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
END = '\033[0m'


def warn(text):
    """ Print the input text to stdout in ANSI red """
    return RED + text + END


def success(text):
    """ Print the input text to stdout in ANSI green """
    return GREEN + text + END


def get_article_links(homepage):
    """ Extract all the article links from the website homepage """
    html = requests.get(homepage).text
    tree = lxml.html.fromstring(html)
    body = tree.find('body')
    body.make_links_absolute(homepage)
    all_urls = [link[2] for link in body.iterlinks()]  # link[2] is the href
    return select_article_links(all_urls)


def select_article_links(url_list):
    """ Select the article links from the entire link list """
    article_links = [
        url for url in url_list
        if re.search(ARTICLE_URL_PATTERN, url)
    ]
    # remove any possible redundancy
    return list(set(article_links))


def scrape(url):
    """ Scrape the target data from a fetched html page """
    # Crawl: fetch html if request status is 200
    req = requests.get(url)
    if req.status_code != 200:  # if something went wrong
        error = "[Error] request on %s returned with status %d (%s)" % (
            url, req.status_code, req.reason)
        print warn(error)
        return None
    html = req.text

    # Parse html: scrape the data using XPaths
    tree = lxml.html.fromstring(html)
    title = tree.xpath('/html/body/div/div/div/div[2]/header/h1/text()')[0]
    author = tree.xpath('/html/body/div/div/div/div[2]/header/p/a/text()')[0]
    date = tree.xpath('/html/body/div/div/div/div[2]/header/div/p/text()')[0]

    # return data as a dict
    data = {'title': title, 'author': author, 'date': date, 'url': url}
    return data


def crawl(article_url_list):
    """ Scrape data from each article page """
    articles_data = []
    for article_url in article_url_list:
        print "Scraping %s" % (article_url)
        scraped = scrape(article_url)
        if scraped:
            print success("[Success] Extracted %s" % (str(scraped)))
            articles_data.append(scraped)
    return articles_data


def main():
    """ Scrape data from all articles at http://isbullsh.it """
    article_urls = get_article_links('http://isbullsh.it')
    print '%d articles found' % (len(article_urls))
    scraped_data = crawl(article_urls)
    dump_file = 'articles.json'
    json.dump(scraped_data, open(dump_file, 'w'), indent=2)
    print '\nAll data has been dumped into %s' % (dump_file)


if __name__ == '__main__':
    main()
