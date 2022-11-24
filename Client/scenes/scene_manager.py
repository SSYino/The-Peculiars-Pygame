from scenes.menu import MenuScreen
from scenes.get_username import GetUsernameScreen

class SceneManager:
    def __init__(self) -> None:
        self.scenes = [MenuScreen("menu"), GetUsernameScreen("getUsername")]
        self.current_scene = None
        self.p = None

    def start(self, p, n):
        self.p = p
        self.net = n
        
        if self.current_scene == None:
            first_scene = MenuScreen("menu")
            self.current_scene = first_scene

            next_scene_name = first_scene.start(p, n)

            while True:
                found_scene = False

                if not next_scene_name:
                    p.RUN = False
                    break
                
                for scene in self.scenes:
                    if scene.get_name() == next_scene_name:
                        found_scene = True
                        next_scene_name = scene.start(p, n)

                if not found_scene:
                    print("not found scene", next_scene_name)
                    


