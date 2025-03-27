
import logging
import yaml
import logging.config

from middlewares.log_filters import RequestIdFilter

def setup_logger():
    """
    Configura o logger da aplicação utilizando o arquivo `logging.yaml`.
    """
    with open("logging.yaml", "r") as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    
    logger = logging.getLogger("root")
    logger.addFilter(RequestIdFilter())

    return logger

logger = setup_logger()

