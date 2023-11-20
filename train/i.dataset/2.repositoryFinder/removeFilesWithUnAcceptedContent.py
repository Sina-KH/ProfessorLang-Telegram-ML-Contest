import os

def remove_files_with_text(directory, text_to_remove):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r', errors='ignore') as file:
                file_content = file.read()
                if text_to_remove in file_content:
                    os.remove(filepath)
                    print(f"Removed: {filename}")

text_to_remove = "assert"

remove_files_with_text("./files/", text_to_remove)