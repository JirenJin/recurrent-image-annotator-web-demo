# Pipeline to start the web demo:

1. In the main project directory (where manage.py exists), run:

```bash
python ipc_server.py
```
to start the RIA server for handling annotation requests.

Then start (maybe in another shell) the demo server by:

```bash
# collect all static files to `STATIC_ROOT`
python manage.py collectstatic
python manage.py runmodwsgi --port=8002
```
