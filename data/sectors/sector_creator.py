import json

############
# Sector 1 #
############

planet_data = [[3500, -200, "Saudor", 100, 0.6, "data\images\celestial\Civilized_Mountains.png", 200],
               [900, 200, "Abyz", 100, 0.6, "data\images\celestial\Civilized_Ice.png", 200]]
star_data = [[2000, 300, "Ion Storm", 450, 2, "data\images\celestial\Star.png", 225]]

sector_data = {"planets":planet_data, "stars":star_data}

with open("sector_1.json", "w") as write_file:
    json.dump(sector_data, write_file) 
