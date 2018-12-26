## Lesson 1
# #1
Words1 = ["разработка", "сокет", "декоратор"]
for w in Words1:
    print ("Слово: ", w, "; Тип:" , type(w))

for w in Words1:
    w = w.encode("utf-8")
    print ("Слово: ", w, "; Тип:" , type(w))

# #2
Words2 = [b"class", b"function", b"method"]
for w in Words2:
    print("Слово: ", w, "; Тип:", type(w), "; Длинна:", len(w))

# #3
Words3 = ["attribute", "класс", "функция", "type"]
for w in Words3:
    try:
        test = w.encode('ascii')
        print(test)
    except:
        print(w," Не возможно преобразовать.")

# #4
Words4 = ["разработка", "администрирование", "protocol", "standard"]
for w in Words4:
    w = w.encode('utf-8')
    print(w)
    w = w.decode('utf-8')
    print(w)

# #5
import subprocess
Res = ["yandex.ru", "youtube.com"]
for r in Res:
    ping = subprocess.Popen(['ping', '-c 3', r], stdout=subprocess.PIPE).stdout
    for line in ping:
        print(line.decode("utf-8").encode('koi8-r')) ## так ? не совсем понятно, что значит на кириллице ?

# #6
Words6 = ["сетевое программирование", "сокет", "декоратор"]
file = open("./test_file.txt", "w")
for w in Words6:
    try:
       file.write(w + "\n")
    except:
        print("Ошибка записи файла.")
file.close()

file2 = open("./test_file.txt", "r", encoding='utf-8')
for l in file2:
    print(l)
