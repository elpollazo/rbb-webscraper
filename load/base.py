from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
import yaml

with open('database_config.yaml', mode='r', encoding='utf-8') as f:
    __config = yaml.load(f)

engine = create_engine(f"mysql+mysqldb://{__config['user']}:{__config['password']}@{__config['host']}:{__config['port']}/{__config['database_name']}")

Session = sessionmaker(bind=engine)

Base = declarative_base()