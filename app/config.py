import os
import sys

configData = []
configData.append({"name": "MAX_CONTENT_LENGTH", "value": 15 * 1024 * 1024})

if os.name == "nt":
    configData.append(
        {
            "name": "STANDARD_FILE_SAVE_FOLDER",
            "value": "app\\static\\\\testing_files\\standard_files\\",
        }
    )
    configData.append(
        {
            "name": "VALIDATE_DOWNLOAD_SAVE_FOLDER",
            "value": os.path.expanduser("~") + "\\Downloads\\",
        }
    )
    configData.append({"name": "MIGRATION_DIR", "value": "app\\migrations"})
elif os.name == "posix" and sys.platform == "darwin":
    configData.append(
        {
            "name": "STANDARD_FILE_SAVE_FOLDER",
            "value": "app/static/testing_files/standard_files/",
        }
    )
    configData.append(
        {
            "name": "VALIDATE_DOWNLOAD_SAVE_FOLDER",
            "value": os.path.expanduser("~") + "/Downloads/",
        }
    )
    configData.append({"name": "MIGRATION_DIR", "value": "app/migrations"})
else:
    configData.append({"name": "STANDARD_FILE_SAVE_FOLDER", "value": ""})
    configData.append({"name": "VALIDATE_DOWNLOAD_SAVE_FOLDER", "value": ""})
    configData.append({"name": "MIGRATION_DIR", "value": ""})


def save_to_env():
    env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
    with open(env_file, "a") as f:
        for cf in configData:
            var = cf["name"]
            value = cf["value"]
            with open(env_file, "r") as file:
                if var in file.read():
                    with open(env_file, "r") as file:
                        lines = file.readlines()
                    with open(env_file, "w") as file:
                        for line in lines:
                            if line.startswith(var):
                                file.write(f"{var}={value}\n")
                            else:
                                file.write(line)
                else:
                    f.write(f"{var}={value}\n")


if __name__ == "__main__":
    save_to_env()
    print("Update config for the current device successfully.")
