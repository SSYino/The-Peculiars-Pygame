from scenes.base_scene import Scene


class CreateGameScreen(Scene):
    def get_name(self):
        return super().get_name()

    def start(self, p, n, m):
        self.run = True
        
        data = {"command": "createGame", "data": {"player_id": m.getState("player")["id"]}}
        n.send_data(data)

        while self.run:
            p.clock.tick(60)
            p.win.fill((128, 128, 128))

            try:
                game_state = m.getState("current_game")

                return {"next_scene": "game"}
            except Exception as e:
                print("no game data received yet")
                font = p.py.font.SysFont("comicsans", 60)
                text = font.render("Creating Game...", 1, (255, 255, 255))
                text_rect = text.get_rect()

                screen_info = p.py.display.Info()
                current_w, current_h = screen_info.current_w, screen_info.current_h
                text_rect.center = (current_w/2, current_h/2)

                p.win.blit(text, text_rect)

            p.py.display.update()

            for event in p.py.event.get():
                if event.type == p.py.QUIT:
                    self.run = False
                    p.py.quit()

    def stop(self):
        return super().stop()
