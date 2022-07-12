"""
This file takes a csv of cines, then 
process data and insert data into the table 
cinesinformation
"""
import re
import os
import pandas as pd
import numpy as np
import datetime
from decouple import config
from connection import get_engine

from loggings import set_up_loggin

logger = set_up_loggin(config("FILE_LOGGER_NAME"))


def find_file():
    folder = "cines"
    subfolder = os.listdir("cines")[-1]
    file = os.listdir(
        os.path.join(folder, subfolder)
    )[-1]
    
    return os.path.join(
        folder, subfolder, file
    )
    

def clean_data():
    """
    This function clean data in
    the cines dataframe
    """
    stress_vowels = {
        "á": "a", "é": "e",
        "í": "i", "ó": "o",
        "ú": "u"
    }
    
    cols_interes = ["Provincia", "Pantallas", "Butacas", "espacio_INCAA"]
    
    df = pd.read_csv(find_file(), encoding="UTF-8")
    
    # lower case
    df["Provincia"] = df["Provincia"].apply(str.lower)
    df["espacio_INCAA"] = df["espacio_INCAA"].apply(
        lambda x: str(x).lower()
    )
    
    # Replacing stress vowels in Provincia
    for key, value in stress_vowels.items():
        df["Provincia"] = df["Provincia"].apply(
            lambda x: re.sub(key, value, str(x))
        )
    
    df["espacio_INCAA"] = df["espacio_INCAA"].replace(
        {"nan": 0, "si": 1, "0": 0}
    )
        
    return df[cols_interes].groupby("Provincia").sum().reindex()
    

def insert_datoscines():
    engine = get_engine(
        config("USER"), 
        config("PASSWORD"), 
        config("HOST"), 
        config("DB_NAME")
    )
        
    df = clean_data()
    
    df.to_sql(
        "datoscines",
        con = engine,
        if_exists="replace",
        index = False
    )


def main_tabla_cines():
    """
    This function execute all this script
    """
    logger.info("The execution of tabla_cines.py started")
    insert_datoscines()
    logger.info("The execution of tabla_cines.py finished")


if __name__ == '__main__':
    main_tabla_cines()