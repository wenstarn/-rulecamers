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

