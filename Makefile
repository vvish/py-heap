requirements:
	pip install -r requirements.txt

tools:
	pip install -r tools.txt

init: requirements tools
	pip install -e .

test:
	py.test

coverage:
	py.test --cov=indexed_heap
	coverage html

.PHONY: init test coverage tools requirements
