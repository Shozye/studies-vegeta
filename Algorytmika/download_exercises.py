
import requests

url = "https://cs.pwr.edu.pl/cichon/2023_24_b/Algorytmika/Zadania/ALGOExercises.pdf"
r = requests.get(url, allow_redirects=True)
with open("ALGOExercises.pdf", 'wb') as file:
    file.write(r.content)