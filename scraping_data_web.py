"""
This script will extract files from pages provided
"""

# Standar library imports
import pandas as pd
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from decouple import config

# Local applications
from loggings import set_up_loggin

# Set up logger
logger = set_up_loggin(config("FILE_LOGGER_NAME"))


def find_url_csv(url: str):
    """
    This function receive the url
    where csv files will be downloaded.
    """
    try: 
        response = requests.get(url)
        if response.ok:
            logger.info("Connection status: Ok")
        else:
            logger.error("Connection status: Fail")
    except HTTPError as http_error: 
        logger.critical(f"{http_error}")
    except Exception as ex:
        logger.error(f"{ex}") 
    
    soup = BeautifulSoup(response.text, features="html.parser")
    tag = soup.find("a", class_="btn btn-green btn-block")
    
    
    return tag.attrs["href"] 
    
        
def download_csv(url):
    try: 
        response = requests.get(url)
        if response.ok:
            logger.info("Connection status: Ok")
            with open("")
        else:
            logger.error("Connection status: Fail")
    except HTTPError as http_error: 
        logger.critical(f"{http_error}")
    except Exception as ex:
        logger.error(f"{ex}") 
    




if __name__ == '__main__':
    find_url_csv("https://datos.gob.ar/dataset/cultura-mapa-cultural-espacios-culturales/archivo/cultura_4207def0-2ff7-41d5-9095-d42ae8207a5d")
