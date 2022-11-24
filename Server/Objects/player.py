class Player:
    def __init__(self, id) -> None:
        self.id = id
        self.display_name = None
        self.current_game_id = None

    def set_display_name(self, name):
        self.display_name = name
        return vars(self)