"""
This script takes a csv file and normalize its content
"""

import pandas as pd
import re

df = pd.read_csv("museos\\2022-July\museos-7-7-2022", encoding="UTF-8")
df2 = pd.read_csv("cines\\2022-July\cines-7-7-2022", encoding="UTF-8")
df3 = pd.read_csv("bibliotecas\\2022-July\\bibliotecas-7-7-2022", encoding="UTF-8")

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

    
        
if __name__ == '__main__':
    print(get_col_of_insterest(df3)["categoria"].unique())
    # rename_cols(df)