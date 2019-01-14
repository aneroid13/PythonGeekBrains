from functools import wraps
from socket import *
import json
import time
import argparse
import logging
from client_log_config import logger_cl as log


def funclogger(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        log.debug(f"Function *{func.__name__}* started with args = { args } and kw-args = {kwargs}")
        result = func(*args, **kwargs)
        if result is not None:
            log.debug(f"Function *{func.__name__}* result = %s", result)
        return result
    return decorator


class JIMClient:
    def __init__(self, addr="localhost", port=7777):
        self.JIMAddress = addr
        self.JIMPort = port
        self.data = None

    def send(self, msg):
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect((self.JIMAddress, self.JIMPort))
            s.send(msg)
            self.data = s.recv(1000000).decode("utf-8")
            s.close()
        except error as ex:
            log.error("Error %s", ex)

    @funclogger
    def get_time(self):
        return time.time()

    @funclogger
    def user_presence(self, username, status):
        template_user_present = {
                "action": "presence",
                "time": self.get_time(),
                "type": "status",
                "user": {
                        "account_name": username,
                        "status": status
                        }
                }

        #JIMMSG = "Hallou !"
        JIMMSG = json.dumps(template_user_present)
        log.debug("Client status answer: %s", JIMMSG.encode("utf-8"))
        self.send(JIMMSG.encode("utf-8"))

    @funclogger
    def srv_answer(self):
        try:
            JIMANSW = json.loads(self.data)
        except (json.JSONDecodeError, TypeError):
            log.warning(f"Incorrect server answer: {self.data}")
            JIMANSW = "Incorrect"

        if JIMANSW is not "Incorrect":
            status_code = int(JIMANSW.get('response'))
            log.debug(f"Code: {status_code}")

            if status_code < 400:
                log.info(JIMANSW.get('alert'))
            else:
                log.error(JIMANSW.get('error'))


def get_args():
    parser = argparse.ArgumentParser(
        description='JIM Server can be started on custom address and port'
    )
    parser.add_argument('-a', '--address', default="0.0.0.0", required=False, action='store', help='Input ip address')
    parser.add_argument('-p', '--port', default=7777, required=False, action='store', help='Input port')
    return parser.parse_args()


if __name__ == "__main__":
    runJIMrun = JIMClient(
        str(get_args().address),
        int(get_args().port)
    )

    runJIMrun.user_presence("It's ME", "Hello")
    runJIMrun.srv_answer()
