from scenes.base_scene import Scene


class MenuScreen(Scene):
    def get_name(self):
        return super().get_name()

    def start(self, p, n, m):
        self.run = True

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
                self.rect.center = (self.x, self.y)

            def update(self, win):
                font = p.py.font.SysFont("comicsans", 40)
                text = font.render(self.text, 1, (255, 255, 255))
                text_rect = text.get_rect()

                text_rect.center = self.rect.center
                win.blit(text, text_rect)

            def click(self, pos):
                return self.rect.collidepoint(pos)

        button_group = p.py.sprite.Group()

        sent_display_name = False

        while self.run:
            p.clock.tick(60)
            p.win.fill((128, 128, 128))

            screen_info = p.py.display.Info()
            current_w, current_h = screen_info.current_w, screen_info.current_h

            try:
                player = m.getState("player")
                if player == None:
                    font = p.py.font.SysFont("comicsans", 60)
                    text = font.render("Loading...", 1 ,(255,255,255))
                    text_rect = text.get_rect()
                    text_rect.center = (current_w/2, current_h/2)
                    p.win.blit(text, text_rect)
                else:
                    if m.init_data and player["display_name"] == None:
                        if not sent_display_name:
                            data = {"command": "setDisplayName", "data": {"player_id": player["id"], "value": m.init_data}}
                            n.send_data(data)
                            sent_display_name = True

                    start_button = Button("Start Game", (current_w)/2, (current_h)/2 - 100, "Gray")
                    join_button = Button("Join Game", (current_w)/2,(current_h)/2 + 100, "Gray")

                    button_group.add([start_button, join_button])
                    button_group.draw(p.win)
                    button_group.update(p.win)

                    button_group.empty()

                for event in p.py.event.get():
                    if event.type == p.py.QUIT:
                        self.run = False
                        p.py.quit()
                    if event.type == p.py.MOUSEBUTTONDOWN:
                        if start_button.click(event.pos):
                            print("start game")
                            if player["display_name"] == None:
                                return {"next_scene": "getUsername", "pending_scene": "createGame"}
                            else:
                                return {"next_scene": "createGame"}
                        elif join_button.click(event.pos):
                            print("join game")
                            if player["display_name"] == None:
                                return {"next_scene": "getUsername", "pending_scene": "joinGame"}
                            else:
                                return {"next_scene": "joinGame"}

                p.py.display.update()
                
            except:
                pass



    def stop(self):
        return super().stop()
