def manager(data, setState):
    command = data["command"]

    def Response(isSuccess, data, comm=command):
        if isSuccess:
            return {"command": comm, "data": data}
        else:
            return {"command": "Unsuccessful", "data": comm}

    match command:
        case "setDisplayName":
            [isSuccess, reply] = setState(data=data)
            return Response(isSuccess, reply)
        case "createGame":
            [isSuccess, reply] = setState(data=data)
            return Response(isSuccess, reply)
        case "joinGame":
            [isSuccess, reply] = setState(data=data)
            return Response(isSuccess, reply)
        case "startGame":
            [isSuccess, reply] = setState(data=data)
            return Response(isSuccess, reply)
        case "getActiveGames":
            [isSuccess, reply] = setState(data=data)
            return Response(isSuccess, reply)
        case "getPlayerData":
            [isSuccess, reply] = setState(data=data)
            return Response(isSuccess, reply, "playerData")
        case _:
            print("Invalid command received in commandsManager")
            return {"command": "Error", "data": "Invalid command"}
