"""This script executes all the complete application"""

from download_source_files import main_download_source_files
from tabla_datos_conjuntos import main_tabla_datos_conjuntos
from tabla_datos_conjuntos import quantity_records_category
from tabla_datos_conjuntos import quantity_records_province_category
from tabla_cines import main_tabla_cines
from sql_execution import create_tables, get_sql_scripts


def main():
    """
    This function perfoms the logic
    of the complete application:
        
        - Extraction of csv files from pages. 
        - Processing the data.
        - Creation of database and tables.
        - Insertion of data into tables
    """
    # Downloading source files
    main_download_source_files()
    
    # SQL files execution 
    create_tables(get_sql_scripts())
    
    # Insertions
    main_tabla_datos_conjuntos() # datosconjuntos table
    main_tabla_cines() # datoscines table
    quantity_records_category() # records x category
    quantity_records_province_category() # records x province and category
    
    
if __name__ == '__main__':    
    main()    