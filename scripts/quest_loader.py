import json
import quest

def load_quest(title):
    sector_file = 'data/quests/' + str(title) + ".json"

    with open(sector_file, "r") as read_file:
        data = json.load(read_file)
    read_file.close()

    mission_list = []

    for line in data:
        mission = quest.Mission(*line) #This might work
        mission_list.append(mission)

    qst = quest.Quest(mission_list)

    return qst


print(load_quest("01A_rendevouz"))

print("Done")