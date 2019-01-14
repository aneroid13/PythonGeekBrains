import logging

logging.basicConfig(
    filename='./log/client_log.txt',
    format='%(asctime)s %(levelname)s %(module)s %(message)s',
    level=logging.DEBUG
)
logger_cl = logging.getLogger("client_logger")