from scenes.menu import MenuScreen
from scenes.get_username import GetUsernameScreen
from scenes.game import GameScreen

class SceneManager:
    def __init__(self, p, net, manager) -> None:
        self.scenes = [MenuScreen("menu"), GetUsernameScreen("getUsername"), GameScreen("game")]
        self.current_scene = None
        self.p = p
        self.net = net
        self.manager = manager

    def start(self):
        if self.current_scene == None:
            first_scene = MenuScreen("menu")
            self.current_scene = first_scene

            next_scene_name = first_scene.start(self.p, self.net, self.manager)

            while True:
                found_scene = False

                if not next_scene_name:
                    self.p.RUN = False
                    break
                
                for scene in self.scenes:
                    if scene.get_name() == next_scene_name:
                        found_scene = True
                        next_scene_name = scene.start(self.p, self.net, self.manager)

                if not found_scene:
                    print("not found scene", next_scene_name)
                    

