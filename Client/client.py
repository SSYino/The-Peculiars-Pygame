print("+ = "+__name__)
from multiprocessing import freeze_support
import sys
import threading
import network
# from config import load_config
from config import action, load_pygame
from scenes.scene_manager import SceneManager
# from config import load_pygame, obj_groups, obj_connect
# from events import events
# from switch import switch
# from items import items
# from action import action, receive
# from communication import communication


def main():
    p = load_pygame.Load()
    scene_manager = SceneManager()
    
    # conn = obj_connect.Load()
    # objs = obj_groups.Load(data, p, conn)
    scenes_thread = threading.Thread(target=scene_manager.start, args=(p, net))
    scenes_thread.start()


    while True:
        # communication(conn, net, app)
        # switch(objs, conn)
        # events(p, objs, conn.FRAME)

        # action(p, objs, data, conn, net)
        action.receive(p, net)

        # items(p, objs, conn)

        if not p.RUN:
            net.end()
            sys.exit()



print("- = "+__name__)

if __name__ == '__main__':
    freeze_support()

    net = network.Load()

    x = threading.Thread(target=net.start, args=())
    y = threading.Thread(target=main, args=())

    y.start()
    x.start()


