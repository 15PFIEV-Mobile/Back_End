# Back_End
1. Run Virtual Environment:
virtualenv --system-site-packages -p python3 ./venv

2. Run Back-end Server:
FLASK_APP=run.py FLASK_DEBUG=1 FLASK_ENV=development flask run --host=0.0.0.0 --port=5000