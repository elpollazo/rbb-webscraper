from sqlalchemy import Column, String, Integer, Text

from base import Base 

class Article(Base):
    __tablename__ = 'articles'

    id = Column(String(200), primary_key=True)
    body = Column(Text())
    host = Column(String(200))
    title = Column(String(200))
    newspaper_uid = Column(String(200))
    n_tokens_title = Column(Integer)
    n_tokens_body = Column(Integer)
    url = Column(String(200), unique=True)

    def __init__(self, uid, body, host, title, newspaper_uid, n_tokens_title, n_tokens_body, url):
        self.id = uid
        self.body = body
        self.host = host
        self.title = title
        self.newspaper_uid = newspaper_uid
        self.n_tokens_title = n_tokens_title
        self.n_tokens_body = n_tokens_body
        self.url = url 