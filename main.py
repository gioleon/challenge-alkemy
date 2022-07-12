"""This script executes all the complete application"""

from tabla_datos_conjuntos import main_tabla_datos_conjuntos
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
    
    # SQL files execution 
    create_tables(get_sql_scripts())
    
    # Insertions
    main_tabla_datos_conjuntos() # datosconjuntos table
    main_tabla_cines() # datoscines table
    
    
if __name__ == '__main__':    
    main()    