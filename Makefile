run:
	@pipenv run python src/manage.py runserver

sync:
	@pipenv run python src/manage.py sync
	@pipenv run python src/manage.py process

lint:
	@pipenv run black .
	@pipenv run isort .

test:
	@pipenv run pytest
