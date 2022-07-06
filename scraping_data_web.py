"""
This script will extract files from pages provided
"""

# Standar library imports
import os
import pandas as pd
import requests
import datetime
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
    
    @param: url of the page where is located the csv file
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
    
        
def download_csv(category, url):
    """
    This function takes the csv's url
    and prepare the file to be downloaded
    
    @param: category of the file will be downloaded
    
    @param: url of the csv file
    """  
    # Dates      
    year = datetime.datetime.now().year
    month = datetime.datetime.now()
    day = datetime.datetime.now().day
    
    # Building path
    path = f"{category}" 
    if not os.path.exists(path):
        os.mkdir(path)
    
    path = os.path.join(path, f"{year}-{month.strftime('%B')}")
    if not os.path.exists(path):
        os.mkdir(path)        
    
    try: 
        response = requests.get(url)
        if response.ok:
            logger.info("Connection status: Ok")
            
            with open(
                os.path.join(path, f"{category}-{day}-{month.month}-{year}"), "wb"
            ) as f:
                f.write(response.content)                      
        else:
            logger.error("Connection status: Fail")
    except HTTPError as http_error: 
        logger.critical(f"{http_error}")
    except Exception as ex:
        logger.error(f"{ex}") 
    

if __name__ == '__main__':
    # Setting categories
    categories = ["MUSEOS", "BIBLIOTECAS", "CINES"]
    
    for i in categories:
        url = find_url_csv(config(i))
        download_csv(i.lower(), url)
    
    