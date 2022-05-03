import json
from ws4py.client.threadedclient import WebSocketClient
from random import randint


class ExampleClient(WebSocketClient):

    def __init__(self, url):
        super().__init__(url)

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        message = json.loads(str(message))
        if "actionList" in message:
            self.send(json.dumps({"actIndex": randint(0, message["indexRange"])}))


if __name__ == '__main__':
    try:
        ws = ExampleClient('ws://127.0.0.1:23456/game/client2')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
