class Receive:
    def __init__(self, net) -> None:
        self.net = net
        self.run = False

    def start(self):
        self.run = True
        q_receive = self.net.q_RECEIVE

        while self.run:
            if not q_receive.empty():
                print(q_receive.get())


# def receive(p, net):
#     if net.q_RECEIVE:
#         print("in action.receive", net.q_RECEIVE)