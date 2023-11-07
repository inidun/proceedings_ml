import os

import jsonlines
import typer


def create_jsonl_from_folder(folder_path: str, output_file: str) -> None:
    """Create a jsonl file from a folder of text files.

    Args:
        folder_path (str): The path to the folder containing the text files.
        output_file (str): The path to the output jsonl file.
    """

    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    with jsonlines.open(output_file, mode='w') as writer:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.txt'):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    content = file.read()
                    writer.write({'text': content, 'meta': {'file_name': file_name}})

if __name__ == "__main__":
    typer.run(create_jsonl_from_folder)
