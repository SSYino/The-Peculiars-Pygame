class Receive:
    def __init__(self, net) -> None:
        self.net = net
        self.run = False
        self.state = {}

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
                    game_dict = data["data"]["game"]
                    new_players = game_dict.pop("players")
                    
                    players_dict = {"old_players": [], "new_players": new_players, "player_count": 0}
                    state["current_game"] = players_dict | game_dict
                except:
                    print("could not create game")
            case _:
                print("Unknown data received")

        print("newState", self.getState())

    def end(self):
        self.run = False


# def receive(p, net):
#     if net.q_RECEIVE:
#         print("in action.receive", net.q_RECEIVE)
