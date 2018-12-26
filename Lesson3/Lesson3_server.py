from socket import *
import json
import time
import argparse

class JIMServer:
    def __init__(self, addr="localhost", port=7777):
        self.JIMAddress = addr
        self.JIMPort = port
        self.clientIP = None
        self.data = None
        self.textanswers = {
            100: "Message",
            101: "Warning",
            200: "OK!",
            201: "Object created.",
            202: "Accepted",
            400: "Wrong request or JSON",
            401: "Not authorized",
            402: "Wrong login or password",
            403: "Forbidden",
            404: "User not found",
            405: "Conflict. Already connected.",
            410: "User offline",
            500: "Server error, something goes wrong."
        }

    def listen(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.JIMAddress, self.JIMPort))
        s.listen(5)

        while True:
            client, addr = s.accept()
            self.clientIP = addr
            self.data = client.recv(1000000)
            status_code = self.check_message()
            client.send(self.answer(status_code, self.textanswers[status_code]))
            client.close()

    def get_time(self):
        return time.time()

    def answer(self, code, msg):

        if code >= 400:
            msgtype = "error"
        else:
            msgtype = "alert"

        template_server_answer = {
            "response": str(code),
            "time": self.get_time(),
            msgtype: str(msg)
                }

        JIMMSG = json.dumps(template_server_answer)
        JIMMSG = JIMMSG.encode("utf-8")
        return JIMMSG

    def check_message(self):
        code = 200
        print(f"Client: {self.clientIP}; Message:{self.data.decode('utf-8')}")

        try:
            JIMREC = json.loads(self.data)

            if JIMREC.get("action") is None or JIMREC.get("time") is None:
                code = 400

        except json.JSONDecodeError:
            code = 400

        return code


def get_args():
    parser = argparse.ArgumentParser(
        description='JIM Server can be started on custom address and port'
    )
    parser.add_argument('-a', '--address', default="0.0.0.0", required=False, action='store', help='Input ip address')
    parser.add_argument('-p', '--port', default=7777, required=False, action='store', help='Input port')
    return parser.parse_args()


if __name__ == "__main__":
    runJIMrun = JIMServer(
        str(get_args().address),
        int(get_args().port)
    )
    runJIMrun.listen()
