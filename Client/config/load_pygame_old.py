import pygame
import pygame_textinput
import network

pygame.font.init()
clock = pygame.time.Clock()

# player = n.getP()
# print("You are player", player["id"])

width = 1250
height = 1000
win = pygame.display.set_mode((width, height), pygame.RESIZABLE )#, pygame.FULLSCREEN)
pygame.display.set_caption("The Peculiars")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 250
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x, self.y))
        # win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


# btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]

def get_username_screen():
    run = True
    textinput = pygame_textinput.TextInputVisualizer()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)

        text = font.render("Enter your display name", 1, (255,0,0))
        win.blit(text, (500,200))

        events = pygame.event.get()
        textinput.update(events)
        win.blit(textinput.surface, (500, 300))

        confirm_button = Button("Confirm", 700, 400, "Gray")
        confirm_button.draw(win)

        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_button.click(event.pos):
                    print("confirmed display name")

                    # Update user display name in Player instance
                    player["display_name"] = textinput.value
                    data = {"command": "set_display_name", "data": textinput.value}
                    n.q_SEND.put(data)

                    # reply = n.send(data)
                    # if not reply:
                    #     run = False
                    #     print("Could not send 'set_display_name'")
                    #     break

                    run = False
                    game_screen()
                    # create_game_screen()

        pygame.display.update()



def create_game_screen():
    run = True
    print("in create game screen")

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        # font = pygame.font.SysFont("comicsans", 60)

        pygame.display.update()

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         exit()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         pass


def game_screen():
    run = True
    # t1 = threading.Thread(target=n.listen, daemon=True)
    # print(t1.daemon, "isDaemon")
    # t1.start()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        
        pygame.display.update()
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
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # redrawWindow(win, game, player)

def menu_screen():
    run = True

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        # font = pygame.font.SysFont("comicsans", 60)

        start_button = Button("Start Game", 500, 300, "Gray")
        join_button = Button("Join Game", 500, 500, "Gray")
        # text = font.render("Click to Play!", 1, (255,0,0))
        # win.blit(text, (100,200))
        # win.blit(start_button, (500,300))
        # win.blit(join_button, (500,500))
        start_button.draw(win)
        join_button.draw(win)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.click(event.pos):
                    print("start game")
                    get_username_screen()
                elif join_button.click(event.pos):
                    print("join game")
                    get_username_screen()


    # main()

if __name__ == '__main__':
    n = network.Load()
    n.start()

    while True:
        menu_screen()
