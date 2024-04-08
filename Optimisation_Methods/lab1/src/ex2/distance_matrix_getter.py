from collections import defaultdict
import json
import re
import sys
import time
from selenium.webdriver.common.by import By

from selenium import webdriver

driver = webdriver.Chrome()

def direction_url(city1: str, city2: str) -> str:
    return f"https://www.google.pl/maps/dir/{city1}/{city2}"

def distance(city1: str, city2: str) -> int:
    if city1 == city2:
        return 0
    driver.get(direction_url(city1, city2)) 
    km_regex = re.compile("<div>\d+ km</div>")
    
    html = driver.page_source
    found = list(map(lambda x: int(x[5:-9]), km_regex.findall(html)))
    while not found:
        time.sleep(1)
        html = driver.page_source
        found = list(map(lambda x: int(x[5:-9]), km_regex.findall(html)))
        
    shortest = min(found)
    print(shortest)

    return int(shortest)

def main():
    url = "https://www.google.pl/maps/"
    distance_matrix: dict[str, dict[str, int]] = defaultdict(dict)
    cities = ["Warszawa","Gdańsk","Szczecin","Wrocław","Kraków","Berlin","Rostok","Lipsk","Praga","Brno","Bratysława","Koszyce","Budapeszt"]

    driver.get(url)
    while driver.title != "Mapy Google":
        time.sleep(1)
        print("Kliknij ten jebany przycisk")
        # W tym czasie kliknij tej jebany przycisk, 
        # ewentualnie zmien zhardkodowany tytul
        
    for c1 in cities:
        for c2 in cities:
            print(f"Check distance {c1} {c2}:", end="")
            distance_matrix[c1][c2] = distance(c1, c2)
            print(distance_matrix[c1][c2])
    
    
    output_string = "\t"
    for c1 in cities:
        output_string += f"{c1} "
    output_string += ":\n"
    for c1 in cities:
        output_string += f"{c1} "
        for c2 in cities:
            output_string += f"{distance_matrix[c1][c2]} "
        output_string += "\n"
    output_string = output_string[:-1] + ";"
    
    with open('distance_matrix.txt', 'w+') as file:
        file.write(output_string)
        file.write("\n\n\n")
        file.write(json.dumps(distance_matrix, indent=4))
    
    
    
            

main()