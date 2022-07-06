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
    formatter = logging.Formatter(
        "%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s"
    )
    
    handler = logging.FileHandler(filename)
    handler.setFormatter(formatter)
    
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    
    
    return logger