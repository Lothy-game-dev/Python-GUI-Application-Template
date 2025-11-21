# E-tax: A Multi-Platform Application for Excel and PDF Processing

## Overview

This is a cross-platform for MacOS and Windows, both desktop and web application designed to process Excel and PDF files efficiently with given requirements. Built using Python’s Flask for web functionalities and PyQt5 for a native graphical user interface (GUI), it enables users to perform file processing tasks across different platforms with ease.

## Key Features

- Process Excel files: Extract, filter, and manipulate data in Excel.
- Process PDF files: Extract, filter, and manipulate text in Excel.
- Web & Desktop Integration: Built using Flask for web and PyQt5 for desktop UI.
- Scalable Deployment: Served with the Waitress WSGI server for production-ready deployment.

## Features

- Excel Processing: Convert, analyze, and manipulate Excel files (.xls, .xlsx).
- PDF Processing: Convert, analyze, and manipulate PDF files (.pdf).
- Data crawling: Crawling travel data from navitime.co.jp for processing.
- Multiplatform: Run as a desktop app using PyQt5 or access through the web with Flask. Can be used on both MacOS and Windows. Read the below for more details on both OS.
- Web Server: Powered by Waitress for lightweight, production-ready web deployment.

## Requirements

Before running the application, ensure you have Python:

- Python 3.12
- pip

Download Python here:

```bash
https://www.python.org/downloads/release/python-3127/
```

Install pip with the following command on Terminal (MacOS):

```bash
python -m ensurepip --upgrade
```

And Command Prompt (Windows):

```bash
cd C:/ # or any folder that contains your Python downloaded
py -m ensurepip --upgrade
```

And the following dependencies installed (if no version is provided, then the newest version will be used):

- PyQt5
- PyQtWebEngine
- pandas
- webdriver_manager
- flask version 2.3.2
- flask-socketio version 5.3.2
- asyncio
- uuid
- pypdfium2
- selenium version 4.21.0
- waitress version 2.1.2
- PyMuPDF
- pdfplumber
- openpyxl
- flask_cors
- xlsxwriter
- eventlet
- python-dotenv
- pytest
- pytest-flask
- flask_sqlalchemy
- flask_migrate
- coverage
- pylint
- black

You can install the required dependencies using the following command:

**On MacOS:**

```bash
make req-mac
```

**On Windows:**

```bash
make req-win
```

## Installation and Setup

**Create Virtual Environment (Optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Incase of python script not working but python3 is working**

Open MacOS Terminal and run the following command:

```bash
sudo ln -s $(which python3) /usr/local/bin/python
```

**Automatically setup .env file based on device**

Change the .env.example file to .env, and run config.py with python

```bash
make config
```

Or you can run as web application once to apply the config file

```bash
make web-run
```

## Running the Application

**1. As a Web Application**

To run the application as a web server:

```bash
make web-run
```

Then, open your browser and visit:

```bash
http://127.0.0.1:5002
```

**2. As an Application**

- On MacOS

To run the application:

```bash
make app-run
```

The application will start after a while.

- On Windows

```bash
make app-run
```

**3. Building the Executable**

To build a standalone executable using PyInstaller:

```bash
make build-mac    # For MacOS
make build-win  # For Windows
```

The standalone executable file and an another application folder will be created in the specified folder.

**4. How to run this app**

Step 1. Navigating to `{path_to_this_project}/app/build/` folder, and choosing the MacOS or Windows folder based on the device's operating system (The other OS's folder might not exist).

Step 2. Run the app using any of the following ways:

- Run the standalone .exe file (Windows) or .app file (MacOS) to run the standalone app, with dependencies bundled inside the app.
- Inside the folder, the will be `_internal` folder which contains the dependecies and the .exe file (Windows) or .app file (MacOS) as the application using the dependencies in `_internal` folder. Run the exe or app file to run this app.

**5. Database**

Run the following scripts:

```bash
make migration
```

This will initialize both migrations and database from models in `app/models` folder if there is no database existed in `app/instance` folder, else it will perform migrations for the existing database in `app/instance` folder.

## Run Unit Tests

**1. Run All Tests**

Run the following command to run all tests:

```bash
make test
```

**1. Flask Application Tests**

All Flask application tests are located in `tests/test_app.py`.

Run the following command to run the tests:

```bash
make test-app
```

**2. Database Tests**

All Database tests are located in `tests/test_database.py`.

Run the following command to run the tests:

```bash
make test-database
```

**3. Generate Coverage Report**

Run the following command to generate the coverage report in terminal:

```bash
make test-report
```

Run the following command to generate the coverage report as html:

```bash
make test-report-html
```

## File Structure

```bash
/project_root
│
├── .venv/                              # Virtual environment for dependencies
│
├── /app                                # Flask application folder
│   │── build/                          # Build folder for multi-platform applications
│   │   │                               # (This folder might be empty on Git, run build based on OS to generate files)
│   │   ├── MacOS/                      # For MacOS
│   │   │   ├── e-Tax.app               # Executable all-in-1 app file
│   │   │   └── e-Tax/                  # Application in a folder
│   │   └── Windows/                    # For Windows
│   │       ├── e-Tax.exe               # Executable all-in-1 exe file
│   │       └── e-Tax/                  # Application in a folder
│   ├── /controllers                    # Controllers for backend
│   ├── /database                       # Database folder
│   │   └── sqlite.py                   # Sqlite initialize script
│   ├── /instance                       # Static files
│   │   └── data.db                     # Sqlite database files (name is dependent on sqlite.py)
│   ├── /migrations                     # Migrations data for database
│   │   ├── /versions                   # Versions folder
│   │   ├── alembic.ini                 # Init files for flask_migrations ---->(only touch if needed)<----
│   │   ├── env.py                      # Init files for flask_migrations ---->(only touch if needed)<----
│   │   ├── README                      # Init files for flask_migrations ---->(only touch if needed)<----
│   │   └── script.py.mako              # Init files for flask_migrations ---->(only touch if needed)<----
│   ├── /models                         # Models for backend
│   ├── /repositories                   # Repositories for backend
│   ├── /static                         # Static files
│   │   ├── /constants                  # Constants JS properties
│   │   ├── /css                        # CSS files
│   │   ├── /images                     # Image files
│   │   ├── /js                         # Javascript files
│   │   └── /testing_files              # Testing template files
│   │       ├── /excel_compare          # Testing input files for excel compare
│   │       ├── /input_files            # Testing input files for e-tax
│   │       ├── /navitime_files         # Testing input files for navitime
│   │       └── /standard_files         # Testing standard files for e-tax
│   ├── /templates                      # HTML templates for the Flask app
│   ├── __init__.py                     # Flask app initialization
│   ├── config.py                       # Configuration settings (dev, prod, etc.)
│   ├── hidden_web_run.py               # Scripts for running the website in hidden mode when building app
│   ├── routes.py                       # Flask routes and views
│   ├── sqlite_process.py               # Flask SQLite database processing scripts
│   └── web_run.py                      # Scripts for running the website independently
│
├── /build                              # Build cache for Pyinstaller (do not touch)
│
├── /gui                                # PyQt5 GUI logic
│   └── main_window.py                  # PyQt5 main window and GUI logic
│
├── /scripts                            # Python scripts for processing files
│   ├── common                          # Common logic functions
│   │   └── main.py                     # Main logic functions
│   ├── e_tax                           # Logic functions for e-tax tab
│   │   ├── color_pdf_file.py           # Coloring errors in pdf file
│   │   ├── color_xlsx_file.py          # Coloring errors in excel file
│   │   ├── helper.py                   # Helper logic functions
│   │   └── main.py                     # Main logic functions
│   ├── excel_compare                   # Logic functions for excel compare tab
│   │   ├── helper.py                   # Helper logic functions
│   │   └── main.py                     # Main logic functions
│   └── navitime                        # Logic functions for navitime tab
│       ├── helper.py                   # Helper logic functions
│       └── main.py                     # Main logic functions
│
├── /specs                              # Specializations files for Windows and MacOS pyinstaller build
│   ├── launcher_windows.spec           # Specializations for Windows
│   └── launcher.spec                   # Specializations for MacOS
│
├── /tests                              # Unit and integration tests
│   ├── test_app.py                     # Testing Flask routes and views
│   ├── test_database.py                # Testing database backend processing
│   ├── test_e_tax.py                   # Testing E Tax files processing
│   ├── test_environment.py             # Environment setup for testing
│   ├── test_gui.py                     # Testing PyQt5 GUI logic
│   └── test_navitime.py                # Testing Navitime Excel processing
│
├── /waitress_server                    # Deployment with Waitress
│   └── server.py                       # Waitress server configuration to serve Flask app
│
├── .coverage                           # Coverage report file
├── .coveragerc                         # Coverage report configuration
├── .env.example                        # Environment file example
├── .gitignore                          # Git ignore file
├── .gitlab-ci.yml                      # Gitlab CI/CD configuration
├── .pylintrc                           # Pylint configuration
├── app_run.py                          # Application running file, used for pyinstaller
├── Makefile                            # Makefile for project (same as package.json)
├── pylint-report.txt                   # Pylint report file
├── README.md                           # Project documentation
├── requirements-windows.txt            # List of dependencies for Windows (Flask, PyQt5, pandas, etc.)
└── requirements.txt                    # List of dependencies for MacOS (Flask, PyQt5, pandas, etc.)
```

## Contributing

Ensure the source code is checked with the following scripts before committing to the repository (will not pass the CI/CD pipeline if not checked).

**1. Linting check**

Run the following command to check the linting:

```bash
make lint
```

**2. Format check**

Run the following command to check the formatting:

```bash
make format-check
```

**3. Auto Format**

Run the following command to format the code:

```bash
make format
```

**4. Unit Test**

Run the following command to run the unit tests:

```bash
make test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions, suggestions, or support, feel free to reach out at [your-email@example.com].
