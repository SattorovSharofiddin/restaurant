mig:
	./manage.py makemigrations
	./manage.py migrate

celery:
	celery -A root worker -l info &
	celery -A root flower --port=5555

req:
	pip freeze > requirements.txt