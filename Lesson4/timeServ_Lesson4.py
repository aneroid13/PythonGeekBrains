# Программа сервера времени
from socket import *
import time


def time_server():
    s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    s.bind(('', 8888))                # Присваивает порт 8888
    s.listen(5)                       # Переходит в режим ожидания запросов;
                                      # одновременно обслуживает не более
                                      # 5 запросов.
    while True:
        client, addr = s.accept()     # Принять запрос на соединение
        print("Получен запрос на соединение от %s" % str(addr))
        timestr = time.ctime(time.time()) + "\n"
        client.send(timestr.encode('utf-8'))
        client.close()


if __name__ == '__main__':
    time_server()
