import socket
import json
import threading
import multiprocessing

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.100"
        self.port = 5555
        self.addr = (self.server, self.port)

        self.q_RECEIVE = multiprocessing.Queue()
        self.q_SEND = multiprocessing.Queue()
        self.q_STATUS = multiprocessing.Queue()

        self.p = self.connect(self.q_SEND, self.q_RECEIVE, self.q_STATUS)

    def getP(self):
        return self.p

    def connect(self, q_send, q_receive, q_status):
        try:
            self.client.connect(self.addr)
            q_status.put({"-1000": "Online"})
            t1 = threading.Thread(target=self.send, args=(q_send,))
            t2 = threading.Thread(target=self.listen, args=(q_receive,))
            player_data = json.loads(self.client.recv(2048).decode())

            t2.start()
            t1.start()
            return player_data
        except:
            q_status.put({"-1000": "Offline"})

    def listen(self, q_receive):
        rec = []
        try:
            while True:
                try:
                    print("listening")
                    rec.append(self.client.recv(2048))
                    data = json.loads(rec.pop().decode())
                    q_receive.put(data)
                    
                    print(data, "just data from server")

                    return data
                except Exception as e:
                    pass

        except Exception as e:
            print(e)
            pass

    def send(self, q_send):
        try:
            while True:
                if not q_send.empty():
                    try:
                        msg = q_send.get()
                        self.client.send(json.dumps(msg).encode())
                    except Exception as e:
                        print(e)
                        break
        # try:
        #     self.client.sendall(str.encode(json.dumps(data)))
        #     recv_data = json.loads(self.client.recv(2048*2).decode())
            
        #     if recv_data:
        #         print(recv_data, "data recv from server after send")
        #         return recv_data
        #     else:
        #         print("no data")
        except socket.error as e:
            print(e)

