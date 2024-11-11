import requests

class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict["nationality"]
        self.team = dict["team"]
        self.assists = dict["assists"]
        self.goals = dict["goals"]
    
    def __str__(self):
        return f"{self.name:20}{self.team} {self.goals} + {self.assists} = {self.goals + self.assists}"
    
class PlayerReader:
    def __init__(self, url):
        response = requests.get(url).json()
        self.players = []
        for player_dict in response:
            player = Player(player_dict)
            self.players.append(player)
        
    def get_players(self):
        return self.players

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader

    def top_scorers_by_nationality(self, nationality):
        all = self.reader.get_players()
        players = []
        for player in all:
            if player.nationality == nationality:
                players.append(player)
        return players