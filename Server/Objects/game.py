class Game:
    def __init__(self, id):
        self.id = id
        self.players = []
        self.current_location = None
        self.current_round = 0

    def __repr__(self) -> str:
        return f"{{id: {self.id}, players: {self.players}}}"

    def get_data(self):
        new_players = []
        for player in self.players:
            new_players.append(player.get_data())
        data = {} | vars(self) | {"players": new_players}
        return data

    def get_game_locations(self):
        # get game locations from a json file
        pass

    def add_player(self, player):
        self.players.append(player)
        return self.players

    def get_game_leader(self):
        return self.players[0]

    def get_game_id(self):
        return self.id

    def get_current_location(self):
        return self.current_location

    def get_current_round(self):
        return self.current_round

    


