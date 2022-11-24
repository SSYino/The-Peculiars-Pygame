import socket
from _thread import *
import json
from Objects.game import Game
from Objects.player import Player

server = "192.168.1.100"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
players = {}
idCount = 0


def threaded_client(conn, addr, p):
    player = Player(p)
    player_dict = vars(player)
    players[p] = player_dict

    data_send(conn, player_dict)

    while True:
        try:
            data = data_get(conn, 4096)

            match data["command"]:
                case "set_display_name":
                    print("set display name")

                    name = data["data"]
                    new_player_dict = player.set_display_name(name)
                    players[p] = new_player_dict

                    data_send(new_player_dict)

                case _:
                    print("Unknown command")

            # if gameId in games:
            #     game = games[gameId]

            #     if not data:
            #         break
            #     else:
            #         if data == "reset":
            #             game.resetWent()
            #         elif data != "get":
            #             game.play(p, data)

            #         conn.sendall(json.dumps(game))
            # else:
            #     break
        except:
            break

    print("Lost connection to", addr)
    # try:
    #     del games[gameId]
    #     print("Closing Game", gameId)
    # except:
    #     pass
    connected.discard(conn)
    conn.close()
    print(connected, "connected members")


def data_get(conn, bytes):
    data = conn.recv(bytes)
    data = json.loads(data.decode())
    return data


def data_send(conn, msg):
    conn.sendall(json.dumps(msg).encode())


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    for sock in connected:
        sock.sendall(json.dumps(
            {"command": "announce", "data": "New user has joined the server"}).encode())

    connected.add(conn)

    start_new_thread(threaded_client, (conn, addr, idCount))
    idCount += 1
