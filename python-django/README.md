# itu-minitwit

## Python setup guide

### Setup and run

Make venv
`python3 -m venv venv`

Go into Venv
`source venv/bin/activate`

Install requirements (if not done)
`pip3 install -r requirements.txt`

```bash
python3 ./manage_prod.py migrate --run-syncdb
python3 ./manage_prod.py collectstatic
python3 ./manage_prod.py runserver 0.0.0.0:5000
```

### Access the App Locally

Once the server is running, visit:
[http://localhost:5000](http://localhost:5000)

If localhost does not work try 127.0.0.1:5000

# How to Run on Raspberry Pi

## Ubuntu Server 24.04.2 LTS

### Default
```bashrc
SECRET_KEY="waect" DATABASE_URL="postgresql://user:password@<ip-address>:5432/waect" python -m gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

### Jemalloc
```bashrc
LD_PRELOAD=/usr/lib/<device specific architecture>/libjemalloc.so.2 SECRET_KEY="waect" DATABASE_URL="postgresql://user:password@<ip-address>:5432/waect" python -m gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```
