import threading
import network
from config import action, load_pygame
from config.scene_manager import SceneManager

def main(p, net, data_manager):
    scene_manager = SceneManager(p, net, data_manager)
    scene_manager.start()

    net.end()
    data_manager.end()


if __name__ == '__main__':
    p = load_pygame.Load()
    net = network.Load()

    # Check for a saved display name
    try:
        with open("data.txt") as file:
            data = file.read()
            key, value = data.split("=")

            data_manager = action.Receive(net, value)
            
    except Exception as e:
        print(e)
        data_manager = action.Receive(net)

    x = threading.Thread(target=data_manager.start, args=())
    y = threading.Thread(target=net.start, args=())

    x.start()
    y.start()

    main(p, net, data_manager)


