class Receive:
    def __init__(self, net, init_data=None) -> None:
        self.net = net
        self.run = False
        self.init_data = init_data
        self.state = {
            "player": None,
            "current_game": None,
            "active_games": None
        }
        # State shape ::
        #     {
        #         "player": {player data},
        #         "current_game": {game data},
        #         "active_games": {
        #             "data": [games data],
        #             "count": int
        #         }
        #     }

    def start(self):
        self.run = True
        q_receive = self.net.q_RECEIVE

        while self.run:
            if not q_receive.empty():
                received = q_receive.get()
                print("Received ---", received)
                self.setState(received)

    def getState(self, key=None):
        if key:
            return self.state[key]

        return self.state

    def setState(self, data):
        state = self.getState()
        match data["command"]:
            case "playerData":
                try:
                    state["player"] = data["data"]
                except:
                    print("could not update player data")
            case "gameData":
                try:
                    state["current_game"] = data["data"]
                except:
                    print("could not update game data")
            case "createPlayer":
                player = data["data"]
                state["player"] = player
            case "setDisplayName":
                try:
                    state["player"]["display_name"] = data["data"]
                except:
                    print("could not set display name")
            case "createGame":
                try:
                    # Update player data
                    new_player_data = data["data"]["player"]
                    state["player"] = new_player_data

                    # Update game data
                    game_data = data["data"]["game"]
                    state["current_game"] = game_data

                except:
                    print("could not create game")
            case "joinGame":
                try:
                    # Update player data
                    new_player_data = data["data"]["player"]
                    state["player"] = new_player_data

                    # Update game data
                    game_data = data["data"]["game"]
                    state["current_game"] = game_data
                except:
                    print("could not join game")
            case "getActiveGames":
                try:
                    state["active_games"] = data["data"]
                except:
                    print("could not set active games in state")
            case _:
                print("Unknown data received")

        print("newState", self.getState())

    def end(self):
        self.run = False
