# This is the class for missions and quests, so I can get an idea of their structure

class Quest():
    def __init__(self, missions):
        self.missions = missions
        self.complete = False
        self.mission_index = 0
        # Iterate through missions, changing the current one
        self.active = True #Create just in time or store?
    
    def check_complete(self):
        if self.missions[self.mission_index].completed:
            # If the current mission is completed,
            if self.mission_index < len(self.missions):
                # and adding one would be in the bounds of the list
                self.mission_index += 1
            elif self.mission_index == len(self.missions):
                self.complete = True

class Mission():
    #Maybe update/check every few frames
    def __init__(self, condition, description, reward, info={}):
        self.completed = False
        self.condition = condition
        # For example, "player.planet.name == 'Abyz'"
        # checks to see if the player has landed on Abyz
        # Each mission checks only ONE condition, quests are containers
        self.description = description
        self.reward = reward
        #{"gold": 100, "experience": 50}
        self.info = info
        # Stores basic information, such as the planet to go to
        # info = {"planet": Abyz}

    def check_condition(self, player): 
        #For performance, only check during certain times (give it quest type, perhaps)
        try:
            check = eval(self.condition)
            #I've heard eval is bad practice for python, maybe look into changing it
        except:
            pass
        else:
            if check:
                print("Yahoo!")
                self.completed = True
                # Give player reward