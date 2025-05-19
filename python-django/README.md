# MiniTwit

## Start application

1. **Reopen in DevContainer**

   codebase comes with the .devcontainer folder which has the minitwit-implemenations container

2. **Run the application**

   ```bash
   python3 ./manage_prod.py migrate --run-syncdb
   python3 ./manage_prod.py collectstatic
   python3 ./manage_prod.py runserver 0.0.0.0:5000
   ```

---

## Access the App

Once the server is running, visit:
[http://localhost:5000](http://localhost:5000)

If localhost does not work try 127.0.0.1:5000
