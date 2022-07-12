"""This script generates the connections to the postgres database"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import exc 
from decouple import config

from loggings import set_up_loggin

# logger
logger = set_up_loggin(config("FILE_LOGGER_NAME"))


def get_engine(user, password, host, db_name):
    """
    This function uses the parameters set in .env file 
    and creates a connection to an existing
    and not existing database.
    """
    url = f"postgresql://{user}:{password}@{host}/{db_name}"
    try:    
        if not database_exists(url):
            create_database(url)
        engine = create_engine(url)
    except exc.SQLAlchemyError as alch_error:
        logger.error(f"{alch_error} in connection.py")
    except Exception as ex:    
        logger.error(f"{ex} in connection.py")
    
    return engine


def get_session():
    """
    This function creates a session using the engine.
    """
    engine = get_engine(config("USER"), config("PASSWORD"), config("HOST"), config("DB_NAME"))
    try:
        session = sessionmaker(bind = engine)()
    except exc.SQLAlchemyError as alch_error:
        logger.error(f"{alch_error} in connection.py")
    except Exception as ex:
        logger.error(f"{ex} in connection.py")
    
    return session


if __name__ == '__main__':
    pass