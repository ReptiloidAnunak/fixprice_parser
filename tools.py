import json

from config import RESULT_JSON

def save_to_result_json_lst(new_data):
    try:
        with open(RESULT_JSON, "r+") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
            data.append(new_data)
            file.seek(0)
            json.dump(data, file, indent=4)

    except FileNotFoundError:
        with open(RESULT_JSON, "w") as file:
            json.dump([new_data], file, indent=4)


