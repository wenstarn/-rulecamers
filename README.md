# Запуск
Запускаем сервер через терминал, выбирая ip и порт

```
python server_final_version.py 127.0.0.1 5555
```
Иницизируем объект класса client, используя ip и порт сервера

```Python
from client_final_version import client
user = client("127.0.0.1", 5555)
```
Далее подключаемся к камере и выполняем какие-нибудь команды, после чего отключаемся

```Python
user.connect_to_camera("172.18.212.17", 80, "laba2102", "TMPpassword")
user.command_to_camera("tilt", 1, 1)
user.command_to_camera("zoom", -1, 1)
user.disconnect_from_camera()
```
После этого можно снова подключиться к камере. По завершению работы необходимо отключиться от сервера

```Python
user.disconnect_from_server()
```
Подробную информацию о работе сервера можно найти в файле log.txt, после вышеописанных операций в нем будет храниться следующее:
```
2020-11-26 19:39:40 User ('127.0.0.1', 55538) successfully connected to camera (172.18.212.17, 80)
2020-11-26 19:39:42 Command move_tilt 1.0 1.0 of User ('127.0.0.1', 55538) for camera (172.18.212.17, 80) was successfully executed
2020-11-26 19:39:43 Command zoom -1.0 1.0 of User ('127.0.0.1', 55538) for camera (172.18.212.17, 80) was successfully executed
2020-11-26 19:39:43 User ('127.0.0.1', 55538) finished work camera with (172.18.212.17, 80)
2020-11-26 19:39:43 User ('127.0.0.1', 55538) disconnected from server
```
