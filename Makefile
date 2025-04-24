ruff:
	poetry run ruff format
	poetry run ruff check --fix

mypy:
	poetry run mypy ./src

pre_commit:
	make ruff
	make mypy

test:
	poetry run pytest .