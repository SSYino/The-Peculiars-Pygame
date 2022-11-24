class Game:
    def __init__(self, id):
        self.id = id
        self.players = None
        self.current_location = None
        self.current_round = 0

    def get_game_locations(self):
        # get game locations from a json file
        pass

    def get_current_location(self):
        return self.current_location

    def get_current_round(self):
        return self.current_round

    


