Repozitoryni clone qilish:

```bash
$ git clone https://github.com/SattorovSharofiddin/restaurant.git .
```
env papkasi yaratish va ushbu papka ichida .env faylini yaratish:
```bash
mkdir env
cd env
touch .env
```
env:
```
# django
SECRET_KEY=''

#redis
REDIS_HOST=redis

# postgres
DB_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_USER=
POSTGRES_DB=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
DATABASE_URL=

#email
EMAIL_BACKEND=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=

#telegram
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=

#mongodb
MONGO_URL=
MONGO_PORT=
MONGO_DB_NAME=
```


Docker-compose orqali ishga tushirish:
```
$ docker-compose up --build
```

http://localhost:8000/
