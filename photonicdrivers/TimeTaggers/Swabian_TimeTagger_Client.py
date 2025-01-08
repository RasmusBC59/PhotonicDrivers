import TimeTagger
from photonicdrivers.Abstract.Connectable import Connectable

class Swabian_TimeTagger_Client(Connectable):
    def __init__(self, ip:str, port:str) -> None:
        self.ip = ip
        self.port = port
    
    def connect(self):
        string = self.ip + ":" + self.port
        print(string)
        self.ttNetwork = TimeTagger.createTimeTaggerNetwork(string)

    def disconnect(self):
        TimeTagger.freeTimeTagger(self.ttNetwork)

    def is_connected(self) -> bool:
        return self.ttNetwork.isConnected()

    def get_model(self):
        return self.ttNetwork.getModel()

if __name__ == "__main__":
    ip = "10.209.67.193"
    port = "41101"
    tt = Swabian_TimeTagger_Client(ip, port)
    tt.connect()