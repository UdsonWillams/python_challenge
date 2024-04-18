run:
	uvicorn app.main:app --reload
coverage:
	coverage run -m unittest
	coverage report --fail-under 100
	coverage html
