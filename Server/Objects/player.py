class Player:
    def __init__(self, id, socket) -> None:
        self.id = id
        self.display_name = None
        self.game_id = None

        self.location = None
        self.role = None

        self._socket = socket

    def __repr__(self) -> str:
        return f"{{id: {self.id}, name: {self.display_name}, game_id: {self.game_id}}}"

    def get_data(self):
        data = {} | vars(self)
        del data["_socket"]
        return data

    def get_limited_data(self):
        data = {} | vars(self)
        del data["_socket"]
        del data["location"]
        del data["role"]
        return data

    def get_socket(self):
        return self._socket

    def get_display_name(self):
        return self.display_name

    def set_display_name(self, name):
        self.display_name = name
        return vars(self)

    def set_location(self, location_name):
        self.location = location_name

    def set_role(self, role):
        self.role = role