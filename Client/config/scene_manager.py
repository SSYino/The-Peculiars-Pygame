from scenes.menu import MenuScreen
from scenes.get_username import GetUsernameScreen
from scenes.create_game import CreateGameScreen
from scenes.join_game import JoinGameScreen
from scenes.game import GameScreen


class SceneManager:
    def __init__(self, p, net, manager) -> None:
        self.scenes = [MenuScreen("menu"), GetUsernameScreen("getUsername"), CreateGameScreen("createGame"), JoinGameScreen("joinGame"), GameScreen("game")]
        self.current_scene = None
        self.p = p
        self.net = net
        self.manager = manager

    def start(self):
        if self.current_scene == None:
            first_scene = MenuScreen("menu")
            self.current_scene = first_scene

            new_scene_data = first_scene.start(self.p, self.net, self.manager)

            while True:
                if not new_scene_data:
                    # print("no new scene data", new_scene_data)
                    self.p.RUN = False
                    break

                found_scene = False
                has_pending_scene = "pending_scene" in new_scene_data and new_scene_data["pending_scene"]
                found_pending_scene = not has_pending_scene

                for scene in self.scenes:
                    if scene.get_name() == new_scene_data["next_scene"]:
                        found_scene = True
                        self.current_scene = scene

                        if has_pending_scene:
                            scene.start(self.p, self.net, self.manager)

                            for scene2 in self.scenes:
                                if scene2.get_name() == new_scene_data["pending_scene"]:
                                    found_pending_scene = True
                                    self.current_scene = scene2
                                    new_scene_data = scene2.start(self.p, self.net, self.manager)
                                    break
                        else:  # No pending scene
                            new_scene_data = scene.start(self.p, self.net, self.manager)
                    
                        break

                if not found_scene:
                    print("not found scene", new_scene_data["next_scene"])
                    new_scene_data = None
                elif not found_pending_scene:
                    print("not found pending scene",
                          new_scene_data["pending_scene"])
                    new_scene_data = None
