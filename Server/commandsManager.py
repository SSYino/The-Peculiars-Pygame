def manager(data, setState):
    command = data["command"]

    def Response(isSuccess, command, data):
        if isSuccess:
            return {"command": command, "data": data}
        else:
            return {"command": "Unsuccessful", "data": command}

    match command:
        case "setDisplayName":
            [isSuccess, reply] = setState(data=data)
            return Response(isSuccess, command, reply)
        case "createGame":
            [isSuccess, reply] = setState(data=data)
            return Response(isSuccess, command, reply)
        case _:
            print("Invalid command received in commandsManager")
            return {"command": "Error", "data": "Invalid command"}
