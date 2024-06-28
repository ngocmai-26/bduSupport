create-venv:
	python -m venv venv

use-venv:
	source venv/Scripts/activate

install-pkg:
	pip install -r requirements.txt

run:
	python manager.py runserver
