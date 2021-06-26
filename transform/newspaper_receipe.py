import argparse
import logging 
import pandas as pd 
from urllib.parse import urlparse
import re
import hashlib
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

logging.basicConfig(level = logging.INFO)

logger = logging.getLogger(__name__)


def main(filename):
    logger.info('Starting cleaning process')
    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _add_host_column(df)
    df = _fill_missing_titles(df)
    df = _add_hashed_uid(df)
    df = _body_modify(df)
    df = _tokenize_column(df, 'title')
    df = _tokenize_column(df, 'body')
    df = _drop_duplicate_values(df, 'title')
    df = _drop_nan_values(df)

    _save_disk(df, filename)

    return df

def _read_data(filename):
    logger.info('Starting reading the data')
    
    return pd.read_csv(filename)

def _extract_newspaper_uid(filename):
    logger.info('Start extracting newspaper uid')
    newspaper_uid = filename.split('_')[0]
    logger.info('Newspaper uid extracted: {}'.format(newspaper_uid))
    
    return newspaper_uid

def _add_newspaper_uid_column(df, newspaper_uid):
    df['newspaper_uid'] = newspaper_uid
    logger.info('Newspaper uid added to dataframe')

    return df

def _add_host_column(df):
    logger.info('Starting spliting host to urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    logger.info('Hosts added')

    return df

def _fill_missing_titles(df):
    logger.info('Start filling missing titles')
    missing_titles_mask = df['title'].isna()
    missing_titles = df[missing_titles_mask]['url'].str.extract(r'(?P<missing_titles>[^/]+)$').applymap(lambda title: title.split('-')).applymap(lambda title: ' '.join(title))
    df.loc[missing_titles_mask, 'title'] = missing_titles.loc[:, 'missing_titles']

    return df

def _add_hashed_uid(df):
    logger.info('Start adding hashed uid')
    uids = (df.apply(lambda row: row['url'], axis=1)
    	      .apply(lambda url: hashlib.md5(bytes(url.encode())))
    	      .apply(lambda hash_obj: hash_obj.hexdigest())
    	    )
    df['uid'] = uids
    df = df.set_index('uid')

    return df

def _body_modify(df):
    logger.info('Start modifying body')
    stripper_body = (df.apply(lambda row: row['body'], axis=1)
    	               .apply(lambda body: list(body))
    	               .apply(lambda letters: (list(map(lambda letter: letter.replace('\n', ''), letters))))
    	               .apply(lambda letters: (list(map(lambda letter: letter.replace('\r', ''), letters))))
    	               .apply(lambda letters: ''.join(letters))
    	            )
    df['body'] = stripper_body

    return df

def _tokenize_column(df, column_name):

    logger.info('Starting tokenize column {}'.format(column_name))
    stop_words = set(stopwords.words("spanish"))
    df['n_tokens_{}'.format(column_name)] = (df.dropna()
            .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
            .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
            .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
            .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
            .apply(lambda valid_words: len(valid_words))
           )
    return df 

def _drop_duplicate_values(df, column):
    
    logger.info('Starting to remove duplicate values')

    return df.drop_duplicates(subset=[column], keep='first')

def _drop_nan_values(df):
	logger.info('Start dropping NaN values')
	return df.dropna()

def _save_disk(df, filename):
    
    clean_filename = 'clean_' + filename
    df.to_csv(clean_filename)
    logger.info('Dataset saved at {}'.format(clean_filename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Filename of csv dirty dataset',
    	type=str)
    args = parser.parse_args()
    main(args.filename)

