import os
import requests

files = [f"gap{i}.txt" for i in "1 2 3 4 5 6 7 8 9 10 11 12 a b c d".split(" ")]

def get_file_url(filename: str) -> str:
    return f"https://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/{filename}"

os.makedirs("data", exist_ok=True)

for filename in files:
    url = get_file_url(filename)
    
    with open(os.path.join("data", filename), 'wb') as file:
        response = requests.get(url)
        file.write(response.content)
        