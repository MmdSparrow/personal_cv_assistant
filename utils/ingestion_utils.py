import json

import fitz


def load_text(txt_file_path):
    with open(txt_file_path, "r", encoding="utf-8") as file_to_read:
        return file_to_read.read()


def load_pdf(pdf_file_path):
    pages = []
    with fitz.open(pdf_file_path) as pdf:
        for page in pdf:
            text = page.get_text("text").strip()
            if text:
                pages.append(text)
    return pages


def load_json(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as file_to_read:
        return json.load(file_to_read)


def json_to_text(data, parent_key=""):
    lines = []
    if isinstance(data, dict):
        for key, value in data.items():
            current_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, (dict, list)):
                lines.extend(json_to_text(value, current_key))
            else:
                lines.append(f"{current_key}: {value}")
    elif isinstance(data, list):
        for index, value in enumerate(data):
            current_key = f"{parent_key}[{index}]"
            if isinstance(value, (dict, list)):
                lines.extend(json_to_text(value, current_key))
            else:
                lines.append(f"{current_key}: {value}")
    else:
        lines.append(f"{parent_key}: {data}")
    return lines
