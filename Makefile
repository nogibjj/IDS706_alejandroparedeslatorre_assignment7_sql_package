install:
	pip install -r requirements.txt
format:
	black *.py
lint:
	ruff check *.py ./lib/*.py
test:
	python -m pytest -vv --nbval -cov=mylib -cov=main test_main.py

run_cli:
	python main.py extract-transform-load
	python main.py create "101" "otro_v2" "175" "12333" "blonde" "green" "blue" "male" "2"
	python main.py read
	python main.py update "101" "otro_v2" "175" "12333" "blonde" "green" "blue" "male" "2"
	python main.py delete "101"

all: install format test lint run_cli