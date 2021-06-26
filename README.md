# rbb-webscraper
This webscraper was used to extract article news from the oficial site of radiobiobio (http://www.biobiochile.cl/) and store them in a MySQL database. Tested on Linux.

Requirements:
- PIP installed.
- MySQL installed.

Libraries used in this web scraper will be installed on "install.sh". The libraries used are:

- Requests.
- Pandas.
- Beautiful Soup.
- SQL Alchemy.
- NLTK.

Ussage:

1. Clone this repository: git clone https://github.com/elpollazo/rbb-webscraper
2. Execute installer file: ./install.sh
4. Insert your MySQL-server credentials on ./load/database_config.yaml file (User, Password, Port, Host, Database name). Database specified in this configuration file must be created if not exists in MySQL server. User must be different than root.
6. To start ETL process: python3 pipeline.py 

Note: ETL proccess will take a while.
