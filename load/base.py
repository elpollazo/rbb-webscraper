from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
import yaml

with open('database_config.yaml', mode='r', encoding='utf-8') as f:
            __config = yaml.load(f)

engine = create_engine('mysql+mysqldb://' + __config['user'] + ':' + __config['password'] + '@' + __config['host'] + ':' + __config['port'] + '/' + __config['database_name'] + '?charset=utf8mb4')

Session = sessionmaker(bind=engine)

Base = declarative_base()