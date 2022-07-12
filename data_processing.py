"""
This script takes a csv file and normalize its content
"""
import re
import os
import pandas as pd
import numpy as np
import datetime
from decouple import config

from loggings import set_up_loggin

# Logger
logger = set_up_loggin(config("FILE_LOGGER_NAME"))


def find_files():
    """
    This function finds CSV files of interest
    
    @return: a list with the lasted CSV files downloaded
    """
    logger.info("Search for the most recent files of interest started")
    
    # Defining path
    folders = ["museos", "cines", "bibliotecas"] # Main folder
     
    subfolder = [] # subfolder
    subfolder.append(os.listdir("museos")[-1])
    subfolder.append(os.listdir("cines")[-1])
    subfolder.append(os.listdir("bibliotecas")[-1])
    
    files = [] # CSV files
    for i in range(3):
        path = folders[i]
        path = os.path.join(path, subfolder[i])
        files.append(os.listdir(path)[-1])
        
    complete_path = []
    for i in range(3):
        complete_path.append(os.path.join(folders[i], subfolder[i], files[i]))

    logger.info("Path of the most recent files found")  
      
    return complete_path 
  
    
def get_col_of_insterest(df: pd.DataFrame):
    """
    This function takes a DataFrame object 
    and normalize its column names, 
    then returns a DataFrame object 
    with solely the columns of interest
    
    @params : DataFrame object
    @return : DataFrame object with solely the columns of interest
    """
    # Dictionaries. Both dictionaries have two elements per line
    stress_vowels = {
        "á": "a", "é": "e",
        "í": "i", "ó": "o",
        "ú": "u"
    }  
      
    col_names = {
        "cod_loc": "cod_localidad", "idprovincia": "id_provincia",
        "iddepartamento": "id_departamento", "categoria": "categoria",
        "provincia": "provincia", "localidad": "localidad",
        "nombre": "nombre", "domicilio": "domicilio",
        "direccion": "domicilio", "cp": "codigo_postal",
        "telefono": "numero_de_telefono", "mail": "mail", 
        "web": "web"
    }
    
    # Column names to lower case
    df = df.rename(str.lower, axis = 1) 
    
    # Replacing stress vowels to normal vowels
    for key, value in stress_vowels.items():
        df = df.rename(
            lambda x: re.sub(key, value, x), axis = 1
        ) 
    
    df = df.rename(col_names, axis = 1)
    
    # Settings columns to filter. 
    cols = list(col_names.values())
    cols.remove("domicilio") # As domicilio is twice, we are deleting one of them.
    
    return df[cols] 


def clean_columns(df: pd.DataFrame): 
    """
    This function takes a dataframe object
    and apply some methods in orden to standarize data.
    (string to lower case, no stress vowels, managment of missing values)
    
    @params : dataframe object
    
    @return : dataframe object with processed data.
    """
    stress_vowels = {
        "á": "a", "é": "e",
        "í": "i", "ó": "o",
        "ú": "u"
    } 
    
    # Columns with strings
    cols = [
        "categoria", "provincia", 
        "localidad", "nombre", 
        "domicilio", "mail", 
        "web"
    ]
    
    # Replacing stress vowels
    df[cols] = df[cols].apply(lambda x: x.str.lower())
    for key, value in stress_vowels.items():
        for col in cols:
            df[col] = df[col].apply(lambda x: re.sub(key, value, str(x)))
            
    # Treating missing values
    cols_missing = df[(df.isnull().sum() > 0).index].columns
    """
    Giving a look at the columns i realized 
    that there are some missing values (nan) present there; 
    however, there are some words that also represent
    missing values (sin direccion, s/n), so, let's unify them. 
    """
    df[cols_missing] = df[cols_missing].replace("sin direccion", np.nan)
    df[cols_missing] = df[cols_missing].replace("s/d", np.nan)
    df[cols_missing] = df[cols_missing].replace("s/n", np.nan)
    df[cols_missing] = df[cols_missing].replace("nan", np.nan)
    
    # deleting spaces within phone numbers
    df["numero_de_telefono"] = df["numero_de_telefono"].apply(
        lambda x: re.sub(" ", "", str(x))
    )
    
    # Changing dtype of columns
    # cols_type = df.select_dtypes("object").columns
    # df[cols_type] = df[cols_type].astype("string")
    
    df[["categoria", "provincia", "localidad"]] = df[[
        "categoria", 
        "provincia", 
        "localidad"
    ]].astype("category")
    
    df[["cod_localidad", "id_provincia", "id_departamento"]] = df[[
        "cod_localidad", "id_provincia", "id_departamento"
    ]].astype("string")
    
    df["fecha_carga"] = datetime.datetime.now()
    
    return df
    
        
def main_data_processing(): 
    """
    This function executed all functions created above.
    """
    logger.info("The execution of data_processing.py started")
    
    complete_path = find_files()
    
    dfs = [] # List of dataframes object with the columns of interest
    for i in complete_path:
        # It create a filtered dataframe 
        dfs.append(get_col_of_insterest(pd.read_csv(i))) 
    
    # concatening dataframes    
    final_df = pd.concat([dfs[0], dfs[1]], ignore_index=True)
    final_df = pd.concat([final_df, dfs[2]], ignore_index=True)   
    
    final_df = clean_columns(final_df)
        
    logger.info("The execution of data_processing.py finished")
    
    return final_df
     
     
if __name__ == '__main__':
    main_data_processing()
    