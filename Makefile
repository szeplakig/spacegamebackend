
install:
	poetry install

flint:
	poetry run ruff format .
	poetry run ruff check --fix .
	poetry run mypy .

lint:
	-poetry run ruff format --check .
	-poetry run ruff check .
	-poetry run mypy .

unit:
	poetry run pytest tests/unit

serve:
	poetry run gunicorn spacegamebackend.service.service:app -k uvicorn.workers.UvicornH11Worker -w 1
