## Chess Tournament project using Django 5.0, DRF.

### Setup

1. Install all package using this command.

```pip install -r requirements.txt```

2. Set your database in `core/settings.py`.
   
4. After than migrate all migrations using this command.
   
```python manage.py migrate```

6. Create Super user.
   
```python manage.py createsuperuser```

8. And you can run now.
   
``` python manage.py runserver 127.0.0.1:8000```

10. You can find API docs with ```https://localhost:8000/docs/``` and admin panel with ```https://localhost:8000/admin```

### Some information
1. If you want set user a admin, you must set ```is_staff=true``` when creating.
2. There is some constants in ```Chess/constants.py```.
3. There is also function for matchmaking without tournament.
4. If you want to run test use ```pytest``` command
5. I used JWT authentication, so if you can send request with bearer auth.
6. To change the duration of access token you can change this in ``settings.py``:

   ```python
   SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_USER': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_USER': timedelta(days=30),
   }

7.

