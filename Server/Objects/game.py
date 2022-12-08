class Game:
    def __init__(self, id):
        self.id = id
        self.players = []
        self.current_location = None
        self.current_round = 0

    def get_data(self):
        return vars(self)

    def get_game_locations(self):
        # get game locations from a json file
        pass

    def add_player(self, player):
        self.players.append(player)

    def get_current_location(self):
        return self.current_location

    def get_current_round(self):
        return self.current_round

    


