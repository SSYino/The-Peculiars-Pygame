from scenes.base_scene import Scene
from config.game_locations import LOCATIONS
from math import floor

class GameScreen(Scene):
    def get_name(self):
        return super().get_name()

    def start(self, p, n, m):
        self.run = True

        class Player(p.py.sprite.Sprite):
            def __init__(self, player_data, player_count, is_me) -> None:
                super().__init__()
                if is_me:
                    self.image = p.py.image.load("assets/images/Logo Yellow.png").convert_alpha()
                else:
                    self.image = p.py.image.load("assets/images/Logo.png").convert_alpha()
                self.image = p.py.transform.scale(self.image, (100, 100))
                self.rect = self.image.get_rect()
                self.rect.midleft = (15, (player_count * 175) + 75)
                self.player_data = player_data
                self.text = self.player_data["display_name"]

            def update(self, win):
                font = p.py.font.SysFont("comicsans", 25)
                text = font.render(self.text, 1, (255, 255, 255))
                text_rect = text.get_rect()

                text_rect.midtop = (self.rect.centerx, self.rect.bottom)
                win.blit(text, text_rect)

        class Location(p.py.sprite.Sprite):
            def __init__(self, location_name, location_num, screen_width, roles) -> None:
                super().__init__()
                self.name = location_name
                self.num = location_num
                self.roles = roles

                self.image = p.py.image.load(f"assets/images/location_background.png").convert()
                # self.image = p.py.image.load(f"assets/images/{self.name}.png").convert_alpha()
                self.img_height = 100
                self.img_width = self.img_height * 1.77765
                self.image = p.py.transform.scale(self.image, (self.img_width, self.img_height))
                self.rect = self.image.get_rect()

                self.startx = 128
                self.locations_per_row = 5
                self.distance_between = ((screen_width - self.startx) / self.locations_per_row) - self.img_width
                self.basex = self.startx + (self.distance_between / 2)
                self.basey = 50
                self.row = floor(location_num / (self.locations_per_row - 0))       # Starts at row 0
                self.column = self.num - ((self.locations_per_row - 0) * self.row)  # Starts at column 0

                self.x = ((self.img_width + self.distance_between) * self.column) + self.basex
                self.y = ((self.img_height + 60) * self.row) + self.basey
                self.rect.topleft = (self.x, self.y)

                font = p.py.font.SysFont("comicsans", 25)
                text = font.render(self.name, 1, (255, 255, 255))
                self.text_rect = text.get_rect()
                self.text_rect.midtop = (self.rect.centerx, self.rect.bottom)
                p.win.blit(text, self.text_rect)

        class Button(p.py.sprite.Sprite):
            def __init__(self, text, x, y, color):
                super().__init__()
                self.text = text
                self.x = x
                self.y = y
                self.width = 250
                self.height = 100
                self.image = p.py.Surface((self.width, self.height))
                self.rect = self.image.get_rect()
                self.color = color
                self.rect.topleft = (self.x, self.y)

            def update(self, win):
                font = p.py.font.SysFont("comicsans", 40)
                text = font.render(self.text, 1, (255, 255, 255))
                text_rect = text.get_rect()

                text_rect.center = self.rect.center
                win.blit(text, text_rect)

            def click(self, pos):
                return self.rect.collidepoint(pos)

        player_group = p.py.sprite.Group()
        location_group = p.py.sprite.Group()
        button_group = p.py.sprite.Group()

        while self.run:
            p.clock.tick(60)
            p.win.fill((128, 128, 128))
            screen_info = p.py.display.Info()
            current_w, current_h = screen_info.current_w, screen_info.current_h

            try:
                game_state = m.getState("current_game")
                if "Err" in game_state:
                    print(game_state['Err'])
                    m.setState({"command": "gameData", "data": None})

                    player_data = m.getState("player")
                    n.send_data({"command": "getPlayerData","data": player_data["id"]})
                    return {"next_scene": "menu"}

                # Players
                me = m.getState("player")
                players = game_state["players"]
                player_count = len(players)
                for count, player_data in enumerate(players):
                    new_player = Player(player_data, count, me["id"] == player_data["id"])
                    player_group.add(new_player)

                # Vertical bar
                p.py.draw.rect(p.win, "black", (125, 0, 3, current_h))

                if not game_state["started"]: # Game is waiting for players
                    # Waiting message
                    font = p.py.font.SysFont("comicsans", 60)
                    text = font.render("Waiting for players...", 1, (255, 255, 255))
                    text_rect = text.get_rect()

                    text_rect.center = (current_w/2, current_h/2)

                    p.win.blit(text, text_rect)

                else: # Game has started

                    # Locations
                    for location_num, location in enumerate(LOCATIONS):
                        location_name = location["name"]
                        location_roles = location["roles"]
                        new_location = Location(location_name, location_num, current_w, location_roles)
                        location_group.add(new_location)

                # Buttons
                game_leader = players[0]
                is_game_leader = me["id"] == game_leader["id"]
                if game_state["started"]: # Game has started
                    # Render role buttons
                    pass
                else: # Game is waiting for players
                    if is_game_leader:
                        if player_count >= game_state["min_players"]:
                            # Render start game button
                            start_button = Button("Start", 125 + 20, current_h - 120, "Black")
                            button_group.add(start_button)

                # Draw
                player_group.draw(p.win)
                player_group.update(p.win)
                button_group.draw(p.win)
                button_group.update(p.win)
                location_group.draw(p.win)

                # print("players", players, "player count", player_count)
            except Exception as e:
                print(f"error {e}")
                print("no players received yet")
                font = p.py.font.SysFont("comicsans", 60)
                text = font.render("No game data", 1, (255, 255, 255))
                text_rect = text.get_rect()

                text_rect.center = (current_w/2, current_h/2)

                p.win.blit(text, text_rect)

            p.py.display.update()
            player_group.empty()
            button_group.empty()
            location_group.empty()
            # try:
            #     game = n.send("get")
            # except:
            #     run = False
            #     print("Couldn't get game")
            #     break

            # if game.bothWent():
            #     redrawWindow(win, game, player)
            #     pygame.time.delay(500)
            #     try:
            #         game = n.send("reset")
            #     except:
            #         run = False
            #         print("Couldn't get game")
            #         break

            # font = pygame.font.SysFont("comicsans", 90)
            # if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
            #     text = font.render("You Won!", 1, (255,0,0))
            # elif game.winner() == -1:
            #     text = font.render("Tie Game!", 1, (255,0,0))
            # else:
            #     text = font.render("You Lost...", 1, (255, 0, 0))

            # win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            # pygame.display.update()
            # pygame.time.delay(2000)

            for event in p.py.event.get():
                if event.type == p.py.QUIT:
                    self.run = False
                    p.py.quit()
                if event.type == p.py.MOUSEBUTTONDOWN:
                    if start_button.click(event.pos):
                        data = {"command": "startGame", "data": {"game_id": game_state["id"], "locations": LOCATIONS}}
                        n.send_data(data)


    def stop(self):
        return super().stop()
