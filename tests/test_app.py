import requests
import numpy as np
import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.__init__ import create_app
from test_environment import frozen_config, reset_frozen_config

# Path to the testing files
testing_project_file_path = "./app/static/testing_files/"
testing_absolute_file_path = "app/static/testing_files/"

# Path to the input files
input_project_file_path = testing_project_file_path + "input_files/"
input_absolute_file_path = testing_absolute_file_path + "input_files/"
input_file_name = [
    "testing-excel-1.xlsx",
    "testing-excel-2.xlsx",
    "testing-excel-3.xlsx",
    "testing-excel-4.xlsx",
    "testing-excel-5.xlsx",
    "testing-pdf-1.pdf",
    "testing-pdf-2.pdf",
    "testing-pdf-3.pdf",
    "testing-pdf-4.pdf",
    "testing-pdf-5.pdf",
]

# Path to the standard file
standard_project_file_path = testing_project_file_path + "standard_files/"
standard_absolute_file_path = testing_absolute_file_path + "standard_files/"
standard_file_name = "mojiichiran.pdf"
base_path = getattr(sys, "_MEIPASS", os.getcwd())

app = None
client = None


@pytest.fixture(scope="session")
def setup_module(request):
    global app, client

    # Set up frozen or non-frozen based on the test case
    if request.param == "frozen":
        frozen_config()  # Simulate frozen state
    else:
        reset_frozen_config()  # Ensure not in frozen state

    app, _ = create_app()
    app.config["TESTING"] = True
    client = app.test_client()

    # Yield so tests run with the appropriate config
    yield

    # Clean up
    reset_frozen_config()


# Test for uploading files
@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_upload_file(setup_module):
    url = "/test/upload"  # Updated the URL to match your route
    random_index = np.random.randint(1, len(input_file_name))
    file_names = [input_file_name[i] for i in range(random_index)]
    file_name_check = {"xlsx_files": [], "pdf_files": []}

    # Prepare the files for uploading
    files = {}
    file_input = []
    for name in file_names:
        if name.endswith(".xlsx"):
            file_name_check["xlsx_files"].append(name)
        elif name.endswith(".pdf"):
            file_name_check["pdf_files"].append(name)
        # Add files for uploading
        file_input.append(
            (open(os.path.join(input_project_file_path, name), "rb"), name)
        )
    files[f"validateFile"] = file_input

    # Perform the POST request with multiple files
    response = client.post(url, data=files)

    # Assert the response
    assert response.status_code == 200
    assert response.json == file_name_check


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_upload_file_failed(setup_module):
    url = "/test/upload"
    response = client.post(url, data={})  # Sending an empty data
    expected_result = {"error": "Bad request"}

    assert response.status_code == 400
    assert response.json == expected_result


# @pytest.mark.parametrize('setup_module', ['frozen', 'non-frozen'], indirect=True)
# def test_standard_file(setup_module):
#     url = "/test/standard"
#     response = client.get(url, query_string={"defaultFile": standard_file_name})
#     expected_result = {
#         "file": base_path + "/" + standard_absolute_file_path + standard_file_name,
#         "file_path": base_path + "/" + standard_absolute_file_path + standard_file_name
#     }

#     assert response.status_code == 200
#     assert response.json == expected_result


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_standard_file_not_found(setup_module):
    url = "/test/standard"
    response = client.get(url, query_string={"defaultFile": "not_exist_file.pdf"})
    expected_result = {"error": "File not found"}

    assert response.status_code == 404
    assert response.json == expected_result


@pytest.mark.parametrize("setup_module", ["frozen", "non-frozen"], indirect=True)
def test_standard_file_empty(setup_module):
    url = "/test/standard"
    response = client.get(url, query_string={})
    expected_result = {"error": "Bad request"}

    assert response.status_code == 400
    assert response.json == expected_result
