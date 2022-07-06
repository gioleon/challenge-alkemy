"""
This script contains the function to create a logger object
"""

import logging


def set_up_loggin(filename: str):
    """"
    This function set up configuration to create the logger.log
    
    @parameter: filename
    @returns: logger object
    """
    
    logger = logging.basicConfig(
        filename = filename, 
        format = "%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s",
        level = logging.DEBUG,
        datefmt = "%H:%M:%S",
        filemode="a"
    )
    
    return logger