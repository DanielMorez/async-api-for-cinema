set_linters:
	echo "ставлю нужные библиотеки"
	pip install  wemake-python-styleguide flake8-html mypy lxml
	mypy --install-types

linters:
	echo "Запускаю isort"
	isort .
	echo "Запускаю flake8"
	flake8 flake8 admin api scheduler user_service worker utils
	echo "Запускаю mypy"
	mapy .
# 	mypy api/src/*
# 	mypy etl/src/*
# 	mypy event_generator/*