from scenes.base_scene import Scene


class GameScreen(Scene):
    def get_name(self):
        return super().get_name()

    def start(self, p, n, m):
        self.run = True
        
        class Player(p.py.sprite.Sprite):
            def __init__(self, player_data, player_count) -> None:
                super().__init__()
                self.image = p.py.image.load("assets/images/Logo.png").convert_alpha()
                self.image = p.py.transform.scale(self.image, (100, 100))
                self.rect = self.image.get_rect()
                self.player_data = player_data
                self.rect.midleft = (15, player_count * 50)


        player_group = p.py.sprite.Group()

        while self.run:
            p.clock.tick(60)
            p.win.fill((128, 128, 128))

            try:
                game_state = m.getState("current_game")
                players = game_state["players"]
                player_count = len(players)
                for count, player_data in enumerate(players):
                    new_player = Player(player_data, count + 1)
                    player_group.add(new_player)

                # new_players = game_state["new_players"]
                # old_players = game_state["old_players"]
                # if new_players:
                #     for player_data in new_players:
                #         player_count = game_state["player_count"]
                #         player_count += 1
                #         new_player  = Player(player_data, player_count)
                #         player_group.add(new_player)

                #         old_players.append(new_players.pop(0))

                player_group.draw(p.win)
                # print("new", new_players, "old", old_players, "player count", player_count)
                print("players", players, "player count", player_count)
            except Exception as e:
                # print(f"error {e}")
                print("no players received yet")
                font = p.py.font.SysFont("comicsans", 60)
                text = font.render("No game data", 1, (255, 255, 255))
                text_rect = text.get_rect()

                screen_info = p.py.display.Info()
                current_w, current_h = screen_info.current_w, screen_info.current_h
                text_rect.center = (current_w, current_h)

                p.win.blit(text, text_rect)



            p.py.display.update()
            player_group.empty()
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

    def stop(self):
        return super().stop()
