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

Ussage:

1. Clone this repository: git clone https://github.com/elpollazo/rbb-webscraper
2. Execute installer file: ./install.sh
3. Insert your mysql-server credentials on ./load/database_config.yaml file (User, Password, Port, Host).
4. To start ETL process type in the project directory: python3 pipeline.py 
