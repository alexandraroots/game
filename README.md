# game

Консольное приложение, которое представляет из себя упрозенную модель экономики игры.

### Перед началом

1. Поднять контейнер с базой:

```
docker pull postgres # скачиваем образа с postgresql
docker run --name postgres-container -e POSTGRES_PASSWORD=test -d -p 5432:5432 postgres
```

2. Накатить handmade миграции на базу:

```
python migrations.py
```

3. Запустить GameServer:
```
uvicorn game.server:app --host 0.0.0.0 --port 8000 # запускаем на локлаьном хосте
```

4. Запустить консольное приложение:
```
python game/client.py
```