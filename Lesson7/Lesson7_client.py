from socket import *
import json
import time
import random
import argparse
import atexit
import logging
from client_log_config import logger_cl as log


class JIMClient:
    def __init__(self, addr="localhost", port=7777):
        self.JIMAddress = addr
        self.JIMPort = port
        self.data = None
        self.username = None
        self.userlogin = False
        self.socket = None

    def connect_server(self):
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect((self.JIMAddress, self.JIMPort))
        except error as ex:
            log.error("Error %s", ex)

    def send(self, msg):
        try:
            self.socket.send(msg)
            self.data = self.socket.recv(1000000).decode("utf-8")
        except error as ex:
            log.error("Error %s", ex)

    def receive(self):
        while True:
            try:
                self.data = None
                self.data = self.socket.recv(1000000).decode("utf-8")
                if self.data is not None:
                    self.srv_answer()
            except error as ex:
                log.error("Error %s", ex)

    def connect_close(self):
        if self.socket != None:
            self.socket.close()

    def get_time(self):
        return time.time()

    def user_presence(self, username, status):
        self.username = username
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
        log.debug(JIMMSG.encode("utf-8"))

        self.connect_server()
        self.send(JIMMSG.encode("utf-8"))

    def send_message(self, to, msg):
        template_chat_message = {
            "action": "msg",
            "time": self.get_time(),
            "to": to,
            "from": self.username,
            "message": msg
        }

        JIMMSG = json.dumps(template_chat_message)
        log.debug(JIMMSG.encode("utf-8"))
        self.send(JIMMSG.encode("utf-8"))

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
                if status_code == 100:
                    print(JIMANSW.get('alert'))
                    log.debug(f"Message: {JIMANSW.get('alert')}")
                if status_code == 200:
                    log.info(f"User connect : {JIMANSW.get('alert')}")
                    self.userlogin = True
            else:
                log.error(f"User connect failed : {JIMANSW.get('error')}")
                self.userlogin = False


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

    may_be = ["Tomas", "Jeremy", "Mike", "Donald"]
    name = random.choice(may_be)
    nikname = name + "_" + str(time.thread_time_ns())[2:5]

    runJIMrun.user_presence(nikname, "I am using JIM Messenger !")
    runJIMrun.srv_answer()
    print("Remeber! you are: " + nikname)
    if runJIMrun.userlogin is True:
        runJIMrun.send_message("#mainroom", f"Hello everybody, I am {nikname} !")
        runJIMrun.receive()

    runJIMrun.connect_close()

