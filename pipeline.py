import logging 
import subprocess
import os
from os import scandir
import re

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
news_sites_uid = ['radiobiobio']

def main():
    _extract()
    _transform()
    _load()
    logger.info('ETL process done')

def _extract():
    """This function executes the extract module. The uncleaned data extracted will be moved to ./transform folder"""
    logger.info('Starting extract process')
    for new_site_uid in news_sites_uid:
        subprocess.run(['python3', 'main.py', '{}'.format(new_site_uid)], cwd='./extract')
        os.system(f'mv ./extract/{new_site_uid}* ./transform')

def _transform():
    """This function executes de transform module. The cleaned data will be moved to ./load folder"""
    logger.info('Starting transform process')

    for new_site_uid in news_sites_uid:
        dirty_data_filename = _get_valid_data_filename(new_site_uid, './transform', type='dirty')
        subprocess.run(['python3', 'newspaper_receipe.py', '{}'.format(dirty_data_filename)], cwd='./transform')
        clean_data_filename = _get_valid_data_filename(new_site_uid, './transform', type='clean')
        os.system(f'mv ./transform/{clean_data_filename} ./load')
        os.system(f'rm ./transform/{dirty_data_filename}')

def _load():
    """This function executes de transform module. The cleaned data will be stored on MySQL database specified on the load configuration"""
    logger.info('Starting load process')
    for new_site_uid in news_sites_uid:
        clean_data_filename = _get_valid_data_filename(new_site_uid, './load', type='clean')
        subprocess.run(['python3', 'main.py', '{}'.format(clean_data_filename)], cwd='./load')
        os.system(f'rm ./load/{clean_data_filename}')
        logger.info('Data loaded into DB')

def _get_valid_data_filename(new_site_uid, wd, type='dirty'):
    """This function scan the current work directory and returns the data file exported in every module"""
    logger.info('Scanning current work directory')

    if type=='dirty':
        valid_file = re.compile(r'^{}_.+_.+_.+_.+csv$'.format(new_site_uid))

        return [filename.name for filename in list(scandir(wd)) if valid_file.match(filename.name)][0]

    elif type=='clean':
        valid_file = re.compile(r'^clean_{}_.+_.+_.+_.+csv$'.format(new_site_uid))

        return [filename.name for filename in list(scandir(wd)) if valid_file.match(filename.name)][0]

if __name__ == '__main__':
    main()
