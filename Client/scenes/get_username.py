from scenes.base_scene import Scene
import pygame_textinput

class GetUsernameScreen(Scene):
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

        textinput = pygame_textinput.TextInputVisualizer()

        while self.run:
            p.clock.tick(60)
            p.win.fill((128, 128, 128))
            font = p.py.font.SysFont("comicsans", 60)

            text = font.render("Enter your display name", 1, (255,0,0))
            p.win.blit(text, (500,200))

            events = p.py.event.get()
            textinput.update(events)
            p.win.blit(textinput.surface, (500, 300))

            confirm_button = Button("Confirm", 700, 400, "Gray")
            confirm_button.draw(p.win)

            for event in events:
                # print(event)
                if event.type == p.py.QUIT:
                    p.py.quit()
                    exit()
                if event.type == p.py.MOUSEBUTTONDOWN:
                    if confirm_button.click(event.pos):
                        print("confirmed display name")

                        # Update user display name in Player instance
                        # player["display_name"] = textinput.value
                        data = {"command": "set_display_name", "data": textinput.value}
                        n.q_SEND.put(data)

                        # reply = n.send(data)
                        # if not reply:
                        #     run = False
                        #     print("Could not send 'set_display_name'")
                        #     break

                        run = False
                        return "gameroom"
                        # create_game_screen()

            p.py.display.update()
