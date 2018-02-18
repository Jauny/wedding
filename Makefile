run:
	. config.env && FLASK_APP=server.py flask run

clean:
	find . -name \*.pyc -delete
