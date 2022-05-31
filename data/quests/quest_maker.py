import json

# 1) Store variables of mission objects in a given json file
# 2) At time of loading, assign the missions to a quest
# NOTE: Each file contains one quest (may be inefficient, but IDC)

################
# Make Mission #
################

# condition, description, reward, info

mission_data = [["player.planet.name == 'Abyz'", "Get to the planet Abyz. Its location will pop up in your stellar compass",
                {"gold": 100, "experience": 50}, {"planet name": 'Abyz'}]]

with open("01A_rendevouz.json", "w") as write_file:
    json.dump(mission_data, write_file)
