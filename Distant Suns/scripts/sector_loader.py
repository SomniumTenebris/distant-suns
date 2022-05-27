import json
import os
import celestial as celeste

def load_sector(num):
    sector_file = "data\sectors\sector_" + str(num) + ".json"

    with open(sector_file, "r") as read_file:
        data = json.load(read_file)
    read_file.close()

    planets = []
    for p in data.get("planets"):
        planet = celeste.Planet(*p)
        planets.append(planet)

    stars = []
    for s in data.get("stars"):
        star = celeste.Star(*p)
        stars.append(star)

    return [planets, stars]
