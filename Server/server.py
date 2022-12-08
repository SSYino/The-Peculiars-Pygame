import socket
import threading
import json
from Objects.game import Game
from Objects.player import Player
from commandsManager import manager

PORT = 5555
SERVER = "localhost"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Server:
    # def __init__(self):
    # self.lobby = Lobby()
    # self.gamerooms = GameRooms(self.lobby)
    # self.keypass = KeyPass()
    # self.database = Database()
    # self.database.create()
    def __init__(self) -> None:
        self.state = {"id_count": 0, "game_id_count": 0}

    def player_thread(self, conn, addr):
        id = self.get_state("id_count")
        player = Player(str(id))

        data = {"command": "createPlayer", "data": player.get_data()}
        self.set_state(data=data)
        self.data_send(conn, data)
        self.set_state("id_count", id + 1)

        run = True
        while run:
            try:
                data = self.data_get(conn, 1024)
                print(data)

                reply = manager(data, self.set_state)
                # if player != None:
                #     self.keypass.start(self, data, conn, player)
                # else:
                #     v = self.database.account(data, conn, addr)
                #     if v[0]:
                #         player = Player(v[3][0], v[3][1], v[3][3], v[3][4], v[3][5], conn, addr)

                self.data_send(conn, reply)

            except Exception as e:
                print("[PLAYER_THREAD]", e)
                run = False

        self.set_state(data={"command": "deletePlayer", "data": {"id": str(id)}})
        conn.close()

    def connection_thread(self):
        try:
            try:
                server.bind((SERVER, PORT))
            except socket.error as e:
                print("[SOCKET]", e)

            print("[SERVER ON]")

            while True:
                try:
                    server.listen()
                    conn, addr = server.accept()
                    print(f"[CONNECT] IP CONNECTED = {addr}")
                    tt = threading.Thread(
                        target=self.player_thread, args=(conn, addr))
                    tt.start()
                except Exception as e:
                    print(f"[Z1] {e}")
        except Exception as e:
            print(f"[Z2] ", e)

    """
     CUSTOM METHODS
    """

    def data_get(self, conn, bytes):
        data = conn.recv(bytes)
        data = json.loads(data.decode())
        return data

    def data_send(self, conn, msg):
        conn.sendall(json.dumps(msg).encode())

    def get_state(self, key=None):
        if key:
            return self.state[key]

        return self.state

    def set_state(self, key=None, value=None, data=None):
        state = self.get_state()
        if key and value:
            state[key] = value
            print("state", self.get_state())
            return True
        elif data:
            [isSuccess, reply] = self.data_manager(state, data)
            print("state", self.get_state())
            return [isSuccess, reply]
        else:
            print("State was not updated")
            return False

    def data_manager(self, state, data):
        match data["command"]:
            case "createPlayer":
                try:
                    if "players" not in state:
                        state["players"] = [data["data"]]
                    else:
                        state["players"].append(data["data"])
                except:
                    print("could not create player")
                    return [False, None]
                return [True, None]

            case "deletePlayer":
                try:
                    player_id = data["data"]["id"]
                    players = state["players"]
                    games = state["games"]
                    for i, player in enumerate(players):
                        if player["id"] == player_id:
                            for i, game in enumerate(games):
                                if game.id == player["game_id"]:
                                    games.pop(i)
                            players.pop(i)
                            break
                except:
                    print("could not delete player")
                    return [False, None]
                return [True, None]

            case "setDisplayName":
                try:
                    player_id = data["data"]["player_id"]
                    display_name = data["data"]["value"]
                    for player in state["players"]:
                        if player["id"] == player_id:
                            player["display_name"] = display_name
                            break
                    
                except:
                    print("could not set display name")
                    return [False, None]
                return [True, display_name]

            case "createGame":
                try:
                    game_id = state["game_id_count"]
                    new_game = Game(str(game_id))
                    self.set_state("game_id_count", game_id + 1)

                    new_player = None
                    player_id = data["data"]["player_id"]
                    for player in state["players"]:
                        if player["id"] == player_id:
                            player["game_id"] = str(game_id)
                            new_player = player
                            new_game.add_player(new_player)
                            break

                    if "games" not in state:
                        state["games"] = [new_game]
                    else:
                        state["games"].append(new_game)

                    reply = {"player": new_player, "game": new_game.get_data()}
                except:
                    print("could not creat game")
                    return [False, None]
                return [True, reply]

            case _:
                print("Unknown command")
                return [False, None]

    # def on_login(self, player):
    #     if player:
    #         self.lobby.add(player)
    #         on_login(player, self.lobby, self.gamerooms)
    #         print(f"{self.time()} [CONNECTED][{player.name}]{player.addr} ")

    # def on_logout(self, player):
    #     if player:
    #         self.gamerooms.disconnected(player)
    #         self.lobby.disconnected(player)
    #         on_logout(player, self.lobby, self.gamerooms)
    #         print(f"{self.time()} [DISCONNECTED][{player.name}]{player.addr} ")


if __name__ == "__main__":
    s = Server()
    t1 = threading.Thread(target=s.connection_thread)
    t1.start()
