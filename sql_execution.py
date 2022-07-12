"""This script create execute sql files to create tables"""
import os
from sqlalchemy.sql import text
from sqlalchemy import exc
from decouple import config
from connection import get_engine

from loggings import set_up_loggin

#
logger = set_up_loggin(config("FILE_LOGGER_NAME"))


def get_sql_scripts():
    """
    This function returns the sql
    files path.
    """
    try:
        scripts = os.listdir("sql_scripts")
    except Exception as ex:
        logger.error(f"{ex} im sql_execution.py")
        
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
            try: 
                with open(os.path.join("sql_scripts", script)) as file:
                    query = text(file.read())
                    con.execute(query)
            except exc.SQLAlchemyError as alche_error:
                logger.error(f"{alche_error} in sql_execution.py")
            except Exception as ex:
                logger.error(f"{ex} in sql_execution.py")
                    

if __name__ == '__main__':
    create_tables(get_sql_scripts())                