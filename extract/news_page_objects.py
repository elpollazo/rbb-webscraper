from common import config
import requests
import bs4

"""This module contains all objects used to do the scrape and extract the data."""

class NewsPage:
    def __init__(self, url, news_site_uid):
        self._config = config()['news_sites'][news_site_uid]
        self._queries = self._config['queries']
        self._html = None
        self._visit(url)
        self.url = url

    def _select(self, query_string):
        """This method is used to do queries in the html parsed object"""
        return self._html.select(query_string)

    def _visit(self, url):
        """Sends a request to the page and get the soup object to do queries"""
        response = requests.get(url)
        response.raise_for_status()
        self._html = bs4.BeautifulSoup(response.text,'html.parser')

class HomePage(NewsPage):
    def __init__(self, url, news_site_uid):
        super().__init__(url, news_site_uid)

    @property
    def get_links(self):
        """Gets the category/article links to do the scrape"""
        categories_links_list = []
        for link in self._select(self._queries['homepage_categories']):
            if link and link.has_attr('href'):
                categories_links_list.append(link)

        return set(link['href'] for link in categories_links_list)

class CategoryHomePage(NewsPage):
    def __init__(self, url, news_site_uid):
        super().__init__(url, news_site_uid)

    @property
    def get_links(self):
        categories_links_list = []
        for link in self._select(self._queries['news_categories']):
            if link and link.has_attr('href'):
                categories_links_list.append(link)

        return set(link['href'] for link in categories_links_list)

class ArticlePage(NewsPage):
    def __init__(self,url ,news_site_uid):
        super().__init__(url, news_site_uid)

    @property
    def title(self):
        """Gets the title of the article news"""
        if requests.get(self.url).encoding == 'ISO-8859-1':
            title = self._select(self._queries['article_title'])
            return title[0].text.encode('latin-1', 'ignore').decode('utf-8', 'ignore') if title else ''

        elif requests.get(self.url).encoding == 'utf-8':
            title = self._select(self._queries['article_title'])
            return title[0].text if title else ''

        else:
            title = self._select(self._queries['article_title'])
            return title[0].text if title else ''

    @property
    def body(self):
        """Gets the body of the article news"""
        if requests.get(self.url).encoding == 'ISO-8859-1':
            body = self._select(self._queries['article_body'])
            return body[0].text.encode('latin-1', 'ignore').decode('utf-8', 'ignore') if body else ''

        elif requests.get(self.url).encoding == 'utf-8':
            body = self._select(self._queries['article_body'])
            return body[0].text if body else ''

        else:
            body = self._select(self._queries['article_body'])
            return body[0].text if body else ''
    


