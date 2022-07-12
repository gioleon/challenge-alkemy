import pandas as pd
from decouple import config
from sqlalchemy import create_engine
from connection import get_engine
from data_processing import main_data_processing
from sql_execution import create_tables, get_sql_scripts

def main():
    engine = get_engine(
        config("USER"), 
        config("PASSWORD"), 
        config("HOST"), 
        config("DB_NAME")
    )
    
    create_tables(get_sql_scripts())
    
    # df
    final_df = main_data_processing()
    
    final_df.to_sql("datosconjuntos", con = engine, if_exists="replace", index = False)

main()    