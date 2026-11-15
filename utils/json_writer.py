import json
import os


def save_json(data: dict, file_path: str):

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )