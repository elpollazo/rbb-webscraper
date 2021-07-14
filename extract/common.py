import yaml
import os

__config = None 

def config(): 
    """This module loads the configuration parameters used to extract the data"""
    global __config
    if not __config:
        with open('config.yaml', mode='r', encoding='utf-8') as f:
            __config = yaml.load(f)
        
    return __config

