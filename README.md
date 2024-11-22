Repozitoryni clone qilish:

```bash
$ git clone https://github.com/SattorovSharofiddin/restaurant.git .
```

Virtual muhitni o'rnatish va aktivlashtirish:
```bash
$ python3 -m venv venv && source venv/bin/activate
```

Kutubhonalarni o'rnatish (Makefile pluginini o'rnatilganini tekshiring):

![image](https://github.com/user-attachments/assets/2f17480d-8443-4fc1-9655-b42b611ef730)

```bash
(venv)$ make req
```
Migratsiyalarni amalga oshirish:
```bash
(venv)$ python manage.py migrate
```
Run the server:
```bash
(venv)$ python manage.py runserver
```
Navigate to http://localhost:8000/ in your favorite web browser.
