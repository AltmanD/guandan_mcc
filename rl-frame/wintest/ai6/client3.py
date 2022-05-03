# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 16:30
# @Author     : Duofeng Wu
# @File       : client.py
# @Description:


import json
from ws4py.client.threadedclient import WebSocketClient
from state3 import State
from action3 import Action


class ExampleClient(WebSocketClient):

    def __init__(self, url):
        super().__init__(url)
        self.state = State()
        self.action = Action()

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        message = json.loads(str(message))                                    # 先序列化收到的消息，转为Python中的字典
        self.state.parse(message)                                             # 调用状态对象来解析状态
        if "actionList" in message:                                           # 需要做出动作选择时调用动作对象进行解析
            act_index = self.action.parse(message)
            self.send(json.dumps({"actIndex": act_index}))


if __name__ == '__main__':
    try:
        # ws = ExampleClient('ws://39.108.189.48:80/game/gd/18762111338284605')
        # # ws = ExampleClient('ws://114.55.107.187:23456/game/18762111338605314')
        # ws = ExampleClient('ws://112.124.24.226:80/game/gd/17550225823901100')
        ws = ExampleClient('ws://112.124.24.226:80/game/gd/17550225823293671')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
