dev:
	uv run gunicorn -w 1 app.main:app --reload