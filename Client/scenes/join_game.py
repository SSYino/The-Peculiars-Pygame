from scenes.base_scene import Scene


class JoinGameScreen(Scene):
    def get_name(self):
        return super().get_name()

    def start(self, p, n, m):
        self.run = True

        getActiveGames = {"command": "getActiveGames", "data": None}

        class Button(p.py.sprite.Sprite):
            def __init__(self, game_id, text, button_num):
                super().__init__()
                self.game_id = game_id
                self.text = text
                self.button_num = button_num
                self.x = (button_num * 250) + 75
                self.y = 180
                self.width = 280
                self.height = self.width / 1.5
                self.image = p.py.image.load("assets/images/game_room.png")
                self.image = p.py.transform.scale(self.image, (self.width, self.height))
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.x, self.y)

            def update(self, win):
                font = p.py.font.SysFont("comicsans", 40)
                text = font.render(self.text, 1, (255, 255, 255))
                text_rect = text.get_rect()

                text_rect.midtop = (self.rect.centerx, self.rect.bottom)
                win.blit(text, text_rect)
                # win.blit(text, self.rect.midleft)
                # win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

            def click(self, pos):
                return self.rect.collidepoint(pos)

        button_group = p.py.sprite.Group()

        while self.run:
            p.clock.tick(60)
            p.win.fill((128, 128, 128))

            font = p.py.font.SysFont("comicsans", 60)
            try:
                n.send_data(getActiveGames)

                active_games = m.getState("active_games")
                text = font.render(f"ACTIVE GAMES: {active_games['count']}", 1, (255, 255, 255))

                for num, game in enumerate(active_games["games_data"]):
                    game_leader = game["game_leader"]
                    game_id = game["game_id"]
                    game_room = Button(game_id, game_leader, num)
                    button_group.add(game_room)

                button_group.draw(p.win)
                button_group.update(p.win)

            except:
                text = font.render("Loading active games...", 1, (255, 255, 255))

            p.win.blit(text, (75, 50))

            # screen_info = p.py.display.Info()
            # current_w, current_h = screen_info.current_w, screen_info.current_h

            # start_button = Button("Start Game", (current_w)/2, (current_h)/2 - 100, "Gray")
            # join_button = Button("Join Game", (current_w)/2,(current_h)/2 + 100, "Gray")
            # win.blit(start_button, (500,300))
            # win.blit(join_button, (500,500))

            p.py.display.update()

            for event in p.py.event.get():
                if event.type == p.py.QUIT:
                    self.run = False
                    p.py.quit()
                if event.type == p.py.MOUSEBUTTONDOWN:
                    for sprite in button_group.sprites():
                        is_clicked = sprite.click(event.pos)
                        if is_clicked:
                            game_id = sprite.game_id
                            print(f"You joined game \"{game_id}\"")

                            data = {"command": "joinGame", "data": {"game_id": game_id, "player_id": m.getState("player")["id"]}}
                            n.send_data(data)

                            return {"next_scene": "game"}
                        break

            button_group.empty()

    def stop(self):
        return super().stop()
