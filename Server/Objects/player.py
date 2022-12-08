class Player:
    def __init__(self, id) -> None:
        self.id = id
        self.display_name = None
        self.game_id = None

    def get_data(self):
        return vars(self)

    def set_display_name(self, name):
        self.display_name = name
        return vars(self)