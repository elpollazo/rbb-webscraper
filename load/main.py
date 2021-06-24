import argparse
import logging
import pandas as pd
import pyodbc
from article import Article

from base import engine, Session, Base


logging.basicConfig(level = logging.INFO)

logger = logging.getLogger(__name__)

def main(filename):

    articles = pd.read_csv(filename)
    connection = engine.raw_connection()
    cursor = connection.cursor()
    #cursor.execute('DROP TABLE IF EXISTS articles;')
    Base.metadata.create_all(engine)
    session = Session()

    for index, row in articles.iterrows():

        logger.info('Loading row uid: {} into DB'.format(row['uid']))
        article = Article(row['uid'],
        	              row['body'],
        	              row['host'],
        	              row['title'],
        	              row['newspaper_uid'],
        	              row['n_tokens_title'],
        	              row['n_tokens_body'],
        	              row['url'])
        session.add(article)
        cursor.execute('ALTER TABLE articles MODIFY body TEXT CHARACTER SET utf8mb4;')
  
    session.commit()
    session.close()
    cursor.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Filename of csv file to load to DB',
    	type=str)
    args = parser.parse_args()
    main(args.filename)