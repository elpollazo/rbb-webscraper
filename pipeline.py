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
    logger.info('Starting extract process')
    for new_site_uid in news_sites_uid:
        subprocess.run(['python3', 'main.py', '{}'.format(new_site_uid)], cwd='./extract')
        #subprocess.run(['mv', '{}*'.format(new_site_uid), r'..\transform'], shell=True, cwd='./extract')
        os.system(f'mv ./extract/{new_site_uid}* ./transform')

def _transform():
    logger.info('Starting transform process')

    for new_site_uid in news_sites_uid:
        dirty_data_filename = _get_valid_data_filename(new_site_uid, './transform', type='dirty')
        subprocess.run(['python3', 'newspaper_receipe.py', '{}'.format(dirty_data_filename)], cwd='./transform')
        clean_data_filename = _get_valid_data_filename(new_site_uid, './transform', type='clean')
        #subprocess.run(['mv', '{}'.format(clean_data_filename), r'..\load'], shell=True, cwd='./transform')
        os.system(f'mv ./transform/{clean_data_filename} ./load')
        #subprocess.run(['rm', '{}'.format(dirty_data_filename)], shell=True, cwd='./transform')
        os.system(f'rm ./transform/{dirty_data_filename}')

def _load():
    logger.info('Starting load process')
    for new_site_uid in news_sites_uid:
        clean_data_filename = _get_valid_data_filename(new_site_uid, './load', type='clean')
        subprocess.run(['python3', 'main.py', '{}'.format(clean_data_filename)], cwd='./load')
        #subprocess.run(['rm', '{}'.format(clean_data_filename)], shell=True, cwd='./load')
        os.system(f'rm ./load/{clean_data_filename}')
        logger.info('Data loaded into DB')

def _get_valid_data_filename(new_site_uid, wd, type='dirty'):
    logger.info('Scanning current work directory')

    if type=='dirty':
        valid_file = re.compile(r'^{}_.+_.+_.+_.+csv$'.format(new_site_uid))

        return [filename.name for filename in list(scandir(wd)) if valid_file.match(filename.name)][0]

    elif type=='clean':
        valid_file = re.compile(r'^clean_{}_.+_.+_.+_.+csv$'.format(new_site_uid))

        return [filename.name for filename in list(scandir(wd)) if valid_file.match(filename.name)][0]

if __name__ == '__main__':
    main()