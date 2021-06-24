import logging 
import subprocess
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
	    subprocess.run(['python', 'main.py', '{}'.format(new_site_uid)], cwd='./extract')
	    subprocess.run(['move', '{}*'.format(new_site_uid), r'..\transform'], shell=True, cwd='./extract')

def _transform():
    logger.info('Starting transform process')

    for new_site_uid in news_sites_uid:
        dirty_data_filename = _get_valid_data_filename(new_site_uid, './transform', type='dirty')
        subprocess.run(['python', 'newspaper_receipe.py', '{}'.format(dirty_data_filename)], cwd='./transform')
        clean_data_filename = _get_valid_data_filename(new_site_uid, './transform', type='clean')
        subprocess.run(['move', '{}'.format(clean_data_filename), r'..\load'], shell=True, cwd='./transform')
        subprocess.run(['del', '{}'.format(dirty_data_filename)], shell=True, cwd='./transform')

def _load():
    logger.info('Starting load process')
    for new_site_uid in news_sites_uid:
        clean_data_filename = _get_valid_data_filename(new_site_uid, './load', type='clean')
        subprocess.run(['python', 'main.py', '{}'.format(clean_data_filename)], cwd='./load')
        subprocess.run(['del', '{}'.format(clean_data_filename)], shell=True, cwd='./load')
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