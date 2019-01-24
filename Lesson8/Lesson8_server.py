from socket import *
import json
import time
import argparse
import select
from queue import Queue
from threading import Thread
from server_log_config import logger_srv as log


class SenderThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_queue = Queue()

    def send(self, item):
        self.input_queue.put(item)

    def close(self):
        self.input_queue.put(None)
        self.input_queue.join()

    def run(self):
        while True:
            item = self.input_queue.get()
            if item is None: break

            client, msg = item

            log.info(f"Server send to: {client['ip']}; User: {client['name']}; Message:{msg}")
            try:
                client['socket'].send(msg)
            except error as er:
                log.error(f"Error: {er}")
                client['socket'].close()

            self.input_queue.task_done()

        self.input_queue.task_done()
        return


class JIMServer:
    def __init__(self, addr="localhost", port=7777):
        self.JIMAddress = addr
        self.JIMPort = port
        self.srv_socket = None
        self.clients = []
        self.to_clients = SenderThread()
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

    def srv_poll(self, mask, timeout):
        poller = select.poll()
        poller.register(self.srv_socket.fileno(), mask)
        return poller.poll(int(timeout * 1000))

    def clinet_poll(self, sock, timeout):
        poller = select.poll()
        poller.register(sock.fileno(), select.POLLIN | select.POLLPRI)
        return poller.poll(int(timeout * 1000))

    def read_events(self, socket):
        if socket is self.srv_socket:
            newsocket, ip = socket.accept()
            newsocket.setblocking(0)
            fd_to_socket = {self.srv_socket.fileno(): self.srv_socket, }
            fd_to_socket[newsocket.fileno()] = newsocket
            poller = select.poll()
            poller.register(newsocket, select.POLLIN | select.POLLPRI)

            socket = newsocket

        data = socket.recv(1000000)
        data = data.decode('utf-8')
        user, code = self.check_message(data)

        for client in self.clients:
            if client['name'] == user:
                client['socket'] = socket
                client['ip'], client['port'] = ip
                self.answer(client, code, self.textanswers[code])

    def newmessage_events(self, socket, client):
        data = socket.recv(1000000)
        data = data.decode('utf-8')
        if data != None:
            data = str.replace(data, "}{", "}&&{")
            for each in str.split(data, "&&"):
                user, code = self.check_message(each)
                self.answer(client, code, self.textanswers[code])

    def error_events(self, socket):
        log.error("Connection refused or client disconnected")
        select.poller.unregister(socket)
        socket.close()

    def init_server(self):
        self.srv_socket = socket(AF_INET, SOCK_STREAM)
        self.srv_socket.setblocking(0)
        self.srv_socket.bind((self.JIMAddress, self.JIMPort))
        self.srv_socket.listen(5)

        self.to_clients.start()  # <- New thread coming

    def listen(self):
        while True:
            try:
                events_in = self.srv_poll(select.POLLIN | select.POLLPRI, 1)
                events_err = self.srv_poll(select.POLLERR | select.POLLHUP, 1)

                fd_to_socket = {self.srv_socket.fileno(): self.srv_socket, }

                for fd, flag in events_in:
                    soc = fd_to_socket[fd]
                    self.read_events(soc)

                for fd, flag in events_err:
                    soc = fd_to_socket[fd]
                    self.error_events(soc)

                for client in self.clients:
                    if client['socket'].fileno() != -1:
                        event_client = self.clinet_poll(client['socket'], 1)
                        fd_to_socket = {client['socket'].fileno(): client['socket'], }

                        for fd, flag in event_client:
                            soc = fd_to_socket[fd]
                            self.newmessage_events(soc, client)
                    else:
                        self.clients.remove(client)

            except error as ex:
                log.error("Error %s", ex)

    def get_time(self):
        return time.time()

    def answer(self, client, code, msg):

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
        log.debug("Server answer : %s", JIMMSG)
        self.to_clients.send((client, JIMMSG))

    def check_message(self, data):
        code = 200
        user = None

        try:
            JIMREC = json.loads(data)

            if JIMREC.get("action") is None or JIMREC.get("time") is None:
                code = 400

        except json.JSONDecodeError:
            code = 400

        if code == 200 and JIMREC.get("action") == "presence":
            user = JIMREC.get("user")['account_name']
            status = JIMREC.get("user")['status']
            self.clients.append({'name': user, 'status': status, 'socket': None, 'ip': None, 'port': None})

        if code == 200 and JIMREC.get("action") == "msg":
            for_who = JIMREC.get("to")
            user = JIMREC.get("from")
            message = JIMREC.get("message")

            if for_who[0] == "#":
                for client in self.clients:
                    self.answer(client, 100, f"|{for_who}| {user}: {message}")
            else:
                for client in self.clients:
                    if client['name'] == for_who:
                        self.answer(client, 100, f"{user}: {message}")

        log.info(f"User: {user}, Message:{data}")

        return user, code


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
    runJIMrun.init_server()
    runJIMrun.listen()
