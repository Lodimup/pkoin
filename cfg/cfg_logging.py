import logging


def config_logging():
    # logging config
    logging.basicConfig(
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO,
                        )
config_logging()
