req-mac:

	pip install -r requirements.txt

req-win:

	pip install -r requirements-windows.txt

config:

	python ./app/config.py

migration:

	python ./app/sqlite_process.py

web-run:

	python ./app/web_run.py

app-run:

	python ./app_run.py

test:

	coverage run -m pytest

test-app:

	coverage run -m pytest ./tests/test_app.py

test-database:

	coverage run -m pytest ./tests/test_database.py

test-report:

	coverage report -m

test-report-html:

	coverage html

build-mac:

	pyinstaller specs/launcher.spec --distpath ./app/build/MacOS

build-win:

	pyinstaller specs/launcher-windows.spec --distpath ./app/build/Windows

PYTHON_FILES_LINT = app/ scripts/

lint:

	@echo "Running pylint on the following directories: $(PYTHON_FILES_LINT)"
	pylint $(PYTHON_FILES_LINT) --output-format=text --rcfile=.pylintrc > pylint-report.txt

PYTHON_FILES_FORMAT = app/ scripts/ waitress_server/ gui/ tests/

format:

	black $(PYTHON_FILES_FORMAT)

format-check:

	black --check $(PYTHON_FILES_FORMAT)
