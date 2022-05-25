import logging
import os
import config


def craete_migration_log(log_file_name: str, module_name: str):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

    os.makedirs(os.path.dirname(log_file_name), exist_ok=True)
    file_handler = logging.FileHandler(config.log_file, mode='w')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return(logger)
