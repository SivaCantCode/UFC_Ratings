import pandas as pd
import requests
from bs4 import BeautifulSoup
import os





data = pd.read_csv(r'FILE_PATH\ufcfights.csv')



class FighterProfile:
    Name = "NULL"
    Rating = 1000
    Class = "NULL"
    Wins = 0
    Loses = 0
    Draws = 0
    NC = 0


    def __init__(self,FighterName):
        self.Name = FighterName
        self.updateClass()

    def getName(self):
       return self.Name

    def getRating(self):
       return self.Rating

    def getClass(self):
        return self.Class

    def updateRating(self,newFighterRating):
        self.Rating = newFighterRating
        self.updateClass()



    def updateClass(self):
        if (self.Rating >= 1200):
            self.Class = "Platnium"
        elif (self.Rating >= 1100):
            self.Class = "Diamond"
        elif (self.Rating >= 1000):
            self.Class = "Gold"
        elif (self.Rating >= 900):
            self.Class = "Silver"
        else:
            self.Class = "Bronze"


            
    def updateRecord (self, FighterRecord):
        self.Record = FighterRecord


    def updateWins(self):
        self.Wins = self.Wins + 1


    def updateLoses(self):
        self.Loses = self.Loses + 1


    def updateDraw(self):
        self.Draws = self.Draws + 1

    def updateNC(self):
        self.NC = self.NC + 1


    def getRecord(self):
        record = str(self.Wins) + "-" + str(self.Loses) +   "-" + str(self.Draws)
        return record




def categorize_method(method):
    if 'KO/TKO' in method:
        return 'KO/TKO'
    elif 'SUB' in method:
        return 'Submission'
    elif 'DEC' in method:
        return 'Decision'
    elif 'DQ' in method:
        return 'Disqualification'
    else:
        return 'Other'





def calcuatePoint (fighter_1 , fighter_2 , multiplier , win_factor , lose_factor):

    rating_a = fighter_1.getRating()
    rating_b = fighter_2.getRating()



    expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    
    expected_b = 1 - expected_a

    base_k = 32
    
    k = base_k * multiplier

    new_rating_a = rating_a + k * ( win_factor - expected_a)
    new_rating_b = rating_b + k * ( lose_factor - expected_b)

    fighter_1.updateRating(round (new_rating_a))
    fighter_2.updateRating(round (new_rating_b))

    
    




def calculateMultiplier (method, winner, loser):

    
    dominance_multipliers = {
        'KO/TKO': 1.5,
        'Submission': 1.5,
        'Decision': 1.0,
        'Disqualification': 0.8,
        'Other': 1.0  
    }


    method_category = categorize_method(method)
    multiplier = dominance_multipliers.get(method_category, 1.0)
    
    
    calcuatePoint(winner,loser,multiplier,1,0)





def get_or_create_fighter(fighter_name, name_map, allFighters_map, index):
    if fighter_name in name_map:
        return name_map[fighter_name], index

    
    new_fighter = FighterProfile(fighter_name)
    allFighters_map[index] = new_fighter
    return new_fighter, index + 1






def process_fights():
    allFighters_map = {}
    i = 101
    for row in data.itertuples():
        name_map = {fighter.Name: fighter for fighter in allFighters_map.values()}
        result = row.result

        # Get or create both fighters
        fighter_1, i = get_or_create_fighter(row.fighter_1, name_map, allFighters_map, i)
        fighter_2, i = get_or_create_fighter(row.fighter_2, name_map, allFighters_map, i)

        if result == "win":
            calculateMultiplier(row.method, fighter_1, fighter_2)
            fighter_1.updateWins()
            fighter_2.updateLoses()
            

        elif result == "draw":
            calcuatePoint(fighter_1, fighter_2, 1, 0.5, 0.5)
            fighter_1.updateDraws()
            fighter_2.updateDraws()

        elif result == "nc":
            fighter_1.updateNC()
            fighter_2.updateNC()

    finalData = []

    for key, fighter in allFighters_map.items():
        print("Loading...")
      


        
        finalData.append({
            "Index": key,
            "Name": fighter.getName(),
            "Rating": fighter.getRating(),
            "Class": fighter.getClass(),
            "Record": fighter.getRecord()
        })

    return finalData


if __name__ == "__main__":
    fighters_data = process_fights()
    





 # df = pd.DataFrame(finalData)




 # df.to_csv("fighters.csv", index=False)

      
    
    
        
        
            
        
    





