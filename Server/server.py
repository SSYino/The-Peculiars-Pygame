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
    def __init__(self) -> None:
        self.state = {"id_count": 0, "game_id_count": 0, "players": [], "games": []}

    def player_thread(self, conn, addr):
        id = self.get_state("id_count")
        player = Player(str(id), conn)

        data_server = {"command": "createPlayer", "data": player}
        data_client = {"command": "createPlayer", "data": player.get_data()}
        self.set_state(data=data_server)
        self.data_send(conn, data_client)
        self.set_state("id_count", id + 1)

        run = True
        while run:
            try:
                data = self.data_get(conn, 1024*4)
                print(data)

                reply = manager(data, self.set_state)
                self.data_send(conn, reply)

            except Exception as e:
                print("[PLAYER_THREAD]", e)
                run = False

        self.set_state(data={"command": "deletePlayer", "data": player.get_data()})
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
        if key and value != None:
            state[key] = value
            print("state", self.get_state())
            return True
        else:
            [isSuccess, reply] = self.data_manager(state, data)
            print("state", self.get_state())
            return [isSuccess, reply]

    def data_manager(self, state, data):
        match data["command"]:
            case "getPlayerData":
                try:
                    player_id = data["data"]
                    for player in state["players"]:
                        if player.id == player_id:
                            return [True, player.get_data()]
                    raise Exception("Could not find player")
                except:
                    print("could not get player data")
                    return [False, None]
            case "createPlayer":
                try:
                    if "players" not in state:
                        state["players"] = [data["data"]]
                    else:
                        state["players"].append(data["data"])
                    return [True, None]
                except:
                    print("could not create player")
                    return [False, None]

            case "deletePlayer":
                try:
                    player = data["data"]
                    players = state["players"]
                    if player["game_id"] == None:
                        for p in players:
                            if p.id == player["id"]:
                                p.id = None
                                break
                    
                    games = state["games"]

                    for i, game in enumerate(games):
                        if game.id == player["game_id"]:
                            games.pop(i)
                            break

                    for p in players:
                        if p.game_id != player["game_id"]:
                            continue

                        if p.id != player["id"] and p.id != None:
                            p.game_id = None
                            game_data = {"command": "gameData", "data": {"Err": "playerDisconnected"}}
                            self.data_send(p.get_socket(), game_data)
                        else:
                            p.id = None

                    new_players_state = [p for p in players if p.id != None]
                    self.set_state("players", new_players_state)

                    return [True, None]
                except Exception as e:
                    print(e)
                    print("could not delete player")
                    return [False, None]

            case "setDisplayName":
                try:
                    player_id = data["data"]["player_id"]
                    display_name = data["data"]["value"]
                    for player in state["players"]:
                        if player.id == player_id:
                            player.set_display_name(display_name)
                            break
                    
                    return [True, display_name]
                except:
                    print("could not set display name")
                    return [False, None]

            case "createGame":
                try:
                    game_id = state["game_id_count"]
                    new_game = Game(str(game_id))
                    self.set_state("game_id_count", game_id + 1)

                    new_player = None
                    player_id = data["data"]["player_id"]
                    for player in state["players"]:
                        if player.id == player_id:
                            player.game_id = str(game_id)
                            new_player = player
                            new_game.add_player(new_player)
                            break

                    if "games" not in state:
                        state["games"] = [new_game]
                    else:
                        state["games"].append(new_game)

                    reply = {"player": new_player.get_data(), "game": new_game.get_data(player_id)}
                    return [True, reply]
                except:
                    print("could not creat game")
                    return [False, None]

            case "joinGame":
                try:
                    game_id = data["data"]["game_id"]
                    player_id = data["data"]["player_id"]
                    game = None
                    player = None

                    for g in state["games"]:
                        if g.get_game_id() == game_id:
                            game = g
                            break
                    for p in state["players"]:
                        if p.id == player_id:
                            player = p
                            break

                    if game and player:
                        player.game_id = game_id
                        players = game.add_player(player)
                        for p in players:
                            game_data = {"command": "gameData", "data": game.get_data(p.id)}
                            if p.id != player.id:
                                self.data_send(p.get_socket(), game_data)
                    else:
                        if not game:
                            print("could not find game")
                        if not player:
                            print("could not find player")
                        raise Exception()

                    reply = {"player": player.get_data(), "game": game.get_data(player.id)}
                    return [True, reply]
                except:
                    print("could not join game")
                    return [False, None]

            case "startGame":
                try:
                    game_id = data["data"]["game_id"]
                    game_locations = data["data"]["locations"]
                    games = state["games"]
                    for game in games:
                        if game.id == game_id:
                            players = game.start(game_locations)
                            for p in players:
                                # Update player state on server
                                for p_state in state["players"]:
                                    if p.id == p_state.id:
                                        p_state.location = p.location
                                        p_state.role = p.role
                                        break

                                # Send game and player data to client
                                game_data = {"command": "gameData", "data": game.get_data(p.id)}
                                player_data = {"command": "playerData", "data": p.get_data()}
                                player_socket = p.get_socket()
                                self.data_send(player_socket, game_data)
                                self.data_send(player_socket, player_data)
                                print("sent data to", p.id)
                            return [True, "Success"]
                except:
                    print("could not start game")
                    return [False, None]

            case "getActiveGames":
                try:
                    games = state["games"]
                    games_count = len(games)
                    games_data = []
                    for game in games:
                        game_leader = game.get_game_leader()
                        game_leader_name = game_leader.get_display_name()
                        game_id = game.get_game_id()
                        games_data.append({"game_id": game_id, "game_leader": game_leader_name})

                    reply = {"games_data": games_data, "count": games_count}
                    return [True, reply]
                except:
                    print("could not get active games")
                    return [False, None]

            case _:
                print("Unknown command")
                return [False, None]


if __name__ == "__main__":
    s = Server()
    t1 = threading.Thread(target=s.connection_thread)
    t1.start()
