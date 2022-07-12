"""This script create execute sql files to create tables"""
import os
from sqlalchemy.sql import text
from decouple import config
from connection import get_engine


def get_sql_scripts():
    """
    This function returns the sql
    files path.
    """
    scripts = os.listdir("sql_scripts")
    
    return scripts
    

def create_tables(scripts: list):
    """
    This functions executes the sql files
    to create tables.
    """
    engine = get_engine(
        config("USER"), 
        config("PASSWORD"), 
        config("HOST"), 
        config("DB_NAME")
    )
    
    for script in scripts:
        with engine.connect() as con:
            with open(os.path.join("sql_scripts", script)) as file:
                query = text(file.read())
                con.execute(query)
                

if __name__ == '__main__':
    create_tables(get_sql_scripts())                