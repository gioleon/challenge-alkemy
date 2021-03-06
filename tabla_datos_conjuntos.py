"""
This script takes a csv, process the data
and then insert that data into dataconjuntos table
"""
import re
import os
import pandas as pd
import numpy as np
import datetime
from decouple import config
from connection import get_engine, get_session
from sqlalchemy.sql import text
from sqlalchemy import exc

from loggings import set_up_loggin

# Logger
logger = set_up_loggin(config("FILE_LOGGER_NAME"))

# engine
engine = get_engine(
        config("USER"), 
        config("PASSWORD"), 
        config("HOST"), 
        config("DB_NAME")
    )

# session
session = get_session()


def find_files():
    """
    This function finds CSV files of interest
    
    @return: a list with the lasted CSV files downloaded
    """
    logger.info("Search for the most recent files of interest started")
    
    # Defining path
    folders = ["museos", "cines", "bibliotecas"] # Main folder
    subfolder = [] # subfolder
    files = [] # CSV files
    
    try: 
        subfolder.append(os.listdir("museos")[-1])
        subfolder.append(os.listdir("cines")[-1])
        subfolder.append(os.listdir("bibliotecas")[-1])
    
    
        for i in range(3):
            path = folders[i]
            path = os.path.join(path, subfolder[i])
            files.append(os.listdir(path)[-1])
    except Exception as ex:
        logger.error(f"{ex} im tabla_datos_conjuntos,py")    
    
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
    
        
def build_final_df(): 
    """
    This function builds the final df
    
    @return: DataFrame object
    """
    
    complete_path = find_files()
    
    dfs = [] # List of dataframes object with the columns of interest
    for i in complete_path:
        # It create a filtered dataframe 
        try:
            dfs.append(get_col_of_insterest(pd.read_csv(i))) 
        except Exception as ex:
            logger.error(f"{ex} in tabla_datos_conjuntos.py")
    # concatening dataframes    
    final_df = pd.concat([dfs[0], dfs[1]], ignore_index=True)
    final_df = pd.concat([final_df, dfs[2]], ignore_index=True)   
    
    final_df = clean_columns(final_df)
    
    return final_df
   
   
def insert_datosconjuntos():
    """
    This function insert information from
    pandas dataframe to sql table
    """
      
    datos_conjuntos = build_final_df()
    
    datos_conjuntos.to_sql(
        "datosconjuntos",
        con = engine, 
        if_exists="replace", 
        index = False
    )
    
    
def quantity_records_category():
    """
    This function execute a query to 
    show the quantity of records are per
    category
    """
    
    with engine.connect() as con:
        try:
            with open("sql_scripts/query_cantidadxcategoria.sql") as file:
                query = text(file.read())
                result = con.execute(query)
        except exc.SQLAlchemyError as alche_error:
            logger.error(f"{alche_error} in tabla_datos_comjuntos") 
       
    pd.DataFrame(result).to_sql(
        "cantidadxcategorias",
        con = engine,
        if_exists ="replace",
        index = False
    )    
       
            
def quantity_records_province_category():
    """
    This function execute a query to 
    show the quantity of records are per
    province and category
    """
    "sql_scripts/cantidadxprovinciaycategorias.sql"
    
    with engine.connect() as con:
        try:
            with open( "sql_scripts/query_cantidadxprovinciaycategorias.sql") as file:
                query = text(file.read())
                result = con.execute(query)    
        except exc.SQLAlchemyError as alche_error:
            logger.error(f"{alche_error} in tabla_datos_comjuntos")  
    
    pd.DataFrame(result).to_sql(
        "cantidadxprovinciaycategorias",
        con = engine,
        if_exists ="replace",
        index = False
    )
        

def main_tabla_datos_conjuntos():
    """
    This function executes the complete file.
    """    
    logger.info("The execution of tabla_datos_conjuntos.py started")
    
    insert_datosconjuntos()
    
    logger.info("The execution of tabla_datos_conjuntos.py finished")
    
          
if __name__ == '__main__':
    main_tabla_datos_conjuntos()
    