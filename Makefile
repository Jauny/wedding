run:
	python wedding.py

test:
	python -m unittest discover -v

clean:
	find . -name \*.pyc -delete
