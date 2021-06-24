import argparse

import logging 

from common import config

import news_page_objects as news

import re

from requests.exceptions import HTTPError

from urllib3.exceptions import MaxRetryError

import datetime

import csv

logging.basicConfig(level = logging.INFO)

logger = logging.getLogger(__name__)

is_well_formed_link = re.compile(r'^https?://.+/?.+$') #https://example.com/bkn
is_root_path = re.compile(r'^/.+$') #/texto
not_valid_link = re.compile(r'^https?://\[.+\]$')

def _news_scrapper(news_site_uid):
    host = config()['news_sites'][news_site_uid]['url']
    logging.info('Beginning scrapprer for {}'.format(host))
    newspage = news.NewsPage(host, news_site_uid)

    if newspage._queries['homepage_categories']:
        homepage = news.HomePage(host, news_site_uid)
        category_host = []
        articles = []

        for link in homepage.get_links:
            category_homepage = _fetch_element(news_site_uid, host, link, 'category')
            if category_homepage:
                logging.info('Category fetched! lel')
                category_host.append(category_homepage)
            else:
                logging.info('Theres no category link')

        for category in category_host:
            if not category.get_links:
    	        logging.warning('This page doesnt have format articles')
            else:
                for article_link in category.get_links:
                    article = _fetch_element(news_site_uid, host, article_link, 'article')
                    if article: 
            	        logging.info('Article fetched!')
            	        articles.append(article)
            	        print(article.title)
                    else:
            	        logging.info('Article not fetched')

    else:

        articles = []
        homepage = news.CategoryHomePage(host, news_site_uid)
        for article_link in homepage.get_links:
            article = _fetch_element(news_site_uid, host, article_link, 'article')
            if article: 
            	logging.info('Article fetched!')
            	articles.append(article)
            	print(article.title)
            else:
                logging.info('Article not fetched')



    _save_articles(articles, news_site_uid)

def _fetch_element(news_site_uid, host, link, element):
    if element == 'article':
        logger.info('Start fetching article at {}'.format(link))
    elif element == 'category':
        logger.info('Start fetching category at {}'.format(link))

    article = None
    category_homepage = None

    try:
    	if element == 'article': 
    	    article = news.ArticlePage(_build_link(host, link), news_site_uid)
    	elif element == 'category':
    	    category_homepage = news.CategoryHomePage(_build_link(host, link), news_site_uid)
    
    except (HTTPError, MaxRetryError) as e:
        logging.warning('Error while fetching the article or category', exc_info=False)

    if article and not article.body:
        logging.warning('Invalid article, there is no body')
        return None

    if element == 'article':
        return article 
    elif element == 'category':
        return category_homepage

def _save_articles(articles, news_site_uid): 

    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = '{site}_{date}_articles.csv'.format(site=news_site_uid,date=now)
    logger.info('Saving articles at: {}'.format(out_file_name))
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(articles[0])))

    with open(out_file_name, mode='w+', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)

        for article in articles:
            row = [str(getattr(article, header)) for header in csv_headers]
            writer.writerow(row)

    logging.info('Articles saved at {}'.format(out_file_name))

def _build_link(host, link):

    if not_valid_link.match(link):
    	return '{}'.format(host)
    elif is_root_path.match(link):
        return '{}{}'.format(host, link)
    elif is_well_formed_link.match(link):
        return link
    else:
        return '{host}/{uri}'.format(host=host, uri=link)

if __name__ == '__main__':

    news_site_choices = list(config()['news_sites'].keys())
    parser = argparse.ArgumentParser()
    parser.add_argument('news_site', help='Sitio de noticias a scrappear',
    	type=str, choices=news_site_choices)
    args = parser.parse_args()
    _news_scrapper(args.news_site)
