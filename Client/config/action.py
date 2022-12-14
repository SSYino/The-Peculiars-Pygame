class Receive:
    def __init__(self, net) -> None:
        self.net = net
        self.run = False
        self.state = {}
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
                    # if "current_game" in state and state["current_game"] is not None:
                    #     pass
                    # else:

                    # Update player data
                    new_player_data = data["data"]["player"]
                    state["player"] = new_player_data

                    # Update game data
                    game_data = data["data"]["game"]
                    state["current_game"] = game_data

                    # game_dict = data["data"]["game"]
                    # new_players = game_dict.pop("players")
                    
                    # players_dict = {"old_players": [], "new_players": new_players, "player_count": 0}
                    # state["current_game"] = players_dict | game_dict
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


# def receive(p, net):
#     if net.q_RECEIVE:
#         print("in action.receive", net.q_RECEIVE)
