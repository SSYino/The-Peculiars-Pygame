from scenes.base_scene import Scene


class MenuScreen(Scene):
    def get_name(self):
        return super().get_name()

    def start(self, p, n):
        self.run = True

        class Button:
            def __init__(self, text, x, y, color):
                self.text = text
                self.x = x
                self.y = y
                self.color = color
                self.width = 250
                self.height = 100

            def draw(self, win):
                p.py.draw.rect(
                    win, self.color, (self.x, self.y, self.width, self.height))
                font = p.py.font.SysFont("comicsans", 40)
                text = font.render(self.text, 1, (255, 255, 255))
                win.blit(text, (self.x, self.y))
                # win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

            def click(self, pos):
                x1 = pos[0]
                y1 = pos[1]
                if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
                    return True
                else:
                    return False

        while self.run:
            p.clock.tick(60)
            p.win.fill((128, 128, 128))
            # font = pygame.font.SysFont("comicsans", 60)

            start_button = Button("Start Game", 500, 300, "Gray")
            join_button = Button("Join Game", 500, 500, "Gray")
            # text = font.render("Click to Play!", 1, (255,0,0))
            # win.blit(text, (100,200))
            # win.blit(start_button, (500,300))
            # win.blit(join_button, (500,500))
            start_button.draw(p.win)
            join_button.draw(p.win)

            p.py.display.update()

            for event in p.py.event.get():
                if event.type == p.py.QUIT:
                    p.py.quit()
                    exit()
                if event.type == p.py.MOUSEBUTTONDOWN:
                    if start_button.click(event.pos):
                        print("start game")
                        return "getUsername"
                    elif join_button.click(event.pos):
                        print("join game")
                        return "getUsername"

    def stop(self):
        return super().stop()