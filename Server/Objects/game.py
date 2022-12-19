from random import choice, randrange

class Game:
    def __init__(self, id):
        self.id = id
        self.min_players = 3
        self.max_players = 10
        self.players = []
        self.started = False
        self.current_location = None
        self.current_round = 0

    def __repr__(self) -> str:
        return f"{{id: {self.id}, players: {self.players}}}"

    def start(self, locations):
        self.started = True

        current_location = choice(locations)
        location_name = current_location["name"]
        location_roles = current_location["roles"]
        self.current_location = location_name

        spy_player_index = randrange(0, len(self.players))
        for i, p in enumerate(self.players):
            if i != spy_player_index:
                # normal player
                role = choice(location_roles)
                p.set_location(location_name)
                p.set_role(role)
            else:
                # spy
                role = "spy"
                p.set_location("Unknown")
                p.set_role(role)

        return self.players

    def get_data(self, self_id):
        new_players = []
        for player in self.players:
            if player.id == self_id:
                new_players.append(player.get_data())
            else:
                new_players.append(player.get_limited_data())
        data = {} | vars(self) | {"players": new_players}
        del data["current_location"]
        
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

    


