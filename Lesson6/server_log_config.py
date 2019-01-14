import logging
import logging.handlers

lformat = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')

fh = logging.handlers.TimedRotatingFileHandler('./log/server_log.txt', 'd', 1, 7, 'utf-8')
fh.setFormatter(lformat)

logger_srv = logging.getLogger("server_logger")
logger_srv.setLevel(logging.DEBUG)
logger_srv.addHandler(fh)
