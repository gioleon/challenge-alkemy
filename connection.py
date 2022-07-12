"""This script generates the connections to the postgres database"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from decouple import config


def get_engine(user, password, host, db_name):
    """
    This function uses the parameters set in .env file 
    and creates a connection to an existing
    and not existing database.
    """
    url = f"postgresql://{user}:{password}@{host}/{db_name}"
    
    if not database_exists(url):
        create_database(url)
    engine = create_engine(url)
    
    return engine


def get_session():
    """
    This function creates a session using the engine.
    """
    engine = get_engine(config("USER"), config("PASSWORD"), config("HOST"), config("DB_NAME"))
    session = sessionmaker(bind = engine)()
    
    return session


if __name__ == '__main__':
    pass