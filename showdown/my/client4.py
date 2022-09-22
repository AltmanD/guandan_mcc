import json
import zmq
from pyarrow import deserialize, serialize
from ws4py.client.threadedclient import WebSocketClient
from random import randint

class ExampleClient(WebSocketClient):
    def __init__(self, url):
        super().__init__(url)
        # 初始化zmq
        self.context = zmq.Context()
        self.context.linger = 0 
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f'tcp://localhost:{6003}')

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        message = json.loads(str(message))
        # 传输给决策模块
        self.socket.send(serialize(message).to_buffer())
        # 收到决策
        act_index = deserialize(self.socket.recv())
        if "actionList" in message:
            self.send(json.dumps({"actIndex": act_index}))


if __name__ == '__main__':
    try:
        ws = ExampleClient('ws://127.0.0.1:23456/game/client0')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
