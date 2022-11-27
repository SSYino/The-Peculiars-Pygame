def manager(data):
    command = data["command"]

    match command:
        case "set_display_name":
            print("Display name", data["data"])
            return {"command": "success", "data": "set_display_name"}
        case _:
            print("Invalid command received in commandsManager")
            return {"command": "Error", "data": "Invalid command"}

