.PHONY: init
init:
	virtualenv venv
	venv/bin/pip install -r requirements.txt
	venv/bin/flask db init
	venv/bin/flask db migrate
	venv/bin/flask db upgrade
	venv/bin/flask seed run
	make test

.PHONY: flask-up
flask-up: 
	FLASK_APP=starnavi.app FLASK_DEBUG=true venv/bin/flask run

.PHONY: test
test:
	venv/bin/python -m pytest -v

.PHONY: db-init
db-init:
	FLASK_APP=starnavi.app venv/bin/flask db init
	FLASK_APP=starnavi.app venv/bin/flask db migrate
	FLASK_APP=starnavi.app venv/bin/flask db upgrade
