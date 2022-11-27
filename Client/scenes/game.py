from scenes.base_scene import Scene


class GameScreen(Scene):
    def get_name(self):
        return super().get_name()

    def start(self, p, n):
        self.run = True

        while self.run:
            p.clock.tick(60)
            p.win.fill((128, 128, 128))
            
            p.py.display.update()
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
                    p.py.quit()
                    exit()

    def stop(self):
        return super().stop()