from datetime import datetime
import os


def save_json(data, path, i):
    with open(f'{path}\\predicted_data_{i}.json', 'w') as f:
        f.write(data)


def save_txt(data, path, i):
    with open(f"{path}\\result_{i}.txt", "w") as f:
        f.write(data)


def create_folder(parent_path: str, name: str) -> str:
    timestamp = datetime.now().strftime('%Y_%m_%d_%I_%M_%S_%p')
    folder_name = f'{name}_output_{timestamp}'

    folder_path: str = os.path.join(parent_path, folder_name)

    os.makedirs(name=folder_path, exist_ok=True)
    return folder_path
