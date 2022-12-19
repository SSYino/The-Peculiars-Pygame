from scenes.base_scene import Scene
import pygame_textinput

class GetUsernameScreen(Scene):
    def get_name(self):
        return super().get_name()

    def start(self, p, n, m):
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
                p.py.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
                font = p.py.font.SysFont("comicsans", 40)
                text = font.render(self.text, 1, (255, 255, 255))
                win.blit(text, (self.x, self.y))

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

            screen_info = p.py.display.Info()
            current_w, current_h = screen_info.current_w, screen_info.current_h

            text = font.render("Enter your display name", 1, (255,255,255))
            text_rect = text.get_rect()
            text_rect.center = (current_w/2, (current_h/2) - 100)
            p.win.blit(text, text_rect)

            events = p.py.event.get()
            textinput.update(events)
            p.win.blit(textinput.surface, ((current_w/2) - 200, (current_h/2) - 50))

            confirm_button = Button("Confirm", (current_w/2) - 125, (current_h/2) + 50, "Gray")
            confirm_button.draw(p.win)

            p.py.display.update()

            for event in events:
                if event.type == p.py.QUIT:
                    self.run = False
                    p.py.quit()
                    return False # Should not continue rendering scenes
                if event.type == p.py.MOUSEBUTTONDOWN:
                    if confirm_button.click(event.pos):
                        print("confirmed display name")

                        name = textinput.value
                        data = {"command": "setDisplayName", "data": {"player_id": m.getState("player")["id"], "value": name}}
                        n.send_data(data)

                        with open("data.txt", "w") as file:
                            file.write(f"name={name}")

                        self.run = False
                        return {"next_scene": "menu"}


    def stop(self):
        return super().stop()