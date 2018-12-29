# Программа клиента, запрашивающего текущее время
from socket import *
import unittest
import time


def get_time():
    s = socket(AF_INET, SOCK_STREAM)  # Создать сокет TCP
    s.connect(('localhost', 8888))   # Соединиться с сервером
    tm = s.recv(1024)                # Принять не более 1024 байтов данных
    s.close()
    return tm


def Mockup_Time_Server():
    return time.ctime(time.time()) + "\n"


class MyTest(unittest.TestCase):

    def setUp(self):
        self.get_local_time = time.ctime(time.time())
        self.get_local_time = self.get_local_time + "\n"  # To be equal time server format

        try:
            self.get_srv_time = get_time().decode("utf-8")

        except ConnectionRefusedError:
            # If we have no time server, than we can mockup
            self.get_srv_time = Mockup_Time_Server()

    def test_time_check(self):
        self.assertEqual(self.get_srv_time, self.get_local_time)

    def test_year2018(self):
        self.assertRegex(self.get_srv_time, "^.*2018$")

    def test_not_year2019(self):
        self.assertNotRegex(self.get_local_time, "^.*2019$")


if __name__ == '__main__':
    unittest.main()

