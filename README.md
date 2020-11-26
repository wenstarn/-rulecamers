# Запуск
Запускаем сервер через терминал, выбирая ip и порт

```
python server 127.0.0.1 5555
```
Иницизируем объект класса client, используя ip и порт сервера

```Python
from client import client
user = client("127.0.0.1", 5555)
```
Далее подключаемся к камере и выполняем какие-нибудь команды, после чего отключаемся

```Python
import time
user.connect_to_camera("172.18.212.17", 80, "laba2102", "TMPpassword")
user.command_to_camera("left", 1, 1)
user.command_to_camera("zoom", 1)
time.sleep(2)
user.command_to_camera("stop")
user.disconnect_from_camera()
```
После этого можно снова подключиться к камере. По завершению работы необходимо отключиться от сервера

```Python
user.disconnect_from_server()
```
Подробную информацию о работе сервера можно найти в файле log.txt, после вышеописанных операций в нем будет храниться следующее:
```
2020-11-26 22:06:46 Connected ('127.0.0.1', 63378)
2020-11-26 22:06:49 User ('127.0.0.1', 63378) successfully connected to camera (172.18.212.17, 80)
2020-11-26 22:06:50 Command left 1.0 1.0 of User ('127.0.0.1', 63378) for camera (172.18.212.17, 80) was successfully executed
2020-11-26 22:06:51 Command zoom 1.0 0.0 of User ('127.0.0.1', 63378) for camera (172.18.212.17, 80) is being executed now
2020-11-26 22:06:53 Command stop of User ('127.0.0.1', 63378) for camera (172.18.212.17, 80) was successfully executed
2020-11-26 22:06:53 User ('127.0.0.1', 63378) finished work camera with (172.18.212.17, 80)
2020-11-26 22:06:53 User ('127.0.0.1', 63378) disconnected from server
```
# Команды камеры
Функция command_to_camera(command, velocity, timeout) принимает три параметра
- command - тип команды
    - left
    - right 
    - up 
    - down
    - zoom
    - stop
- velocity - скорость движения(по умолчанию равно 1)
- timeout - время движения(если не указать значение, то движение прекратиться только когда пользователь использует команду "stop")



