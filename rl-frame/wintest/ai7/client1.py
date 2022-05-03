# -*- coding: utf-8 -*-
# @Time       : 2020/10/19 19:30
# @Author     : Duofeng Wu  &&  Zenghui Qian
# @File       : client.py
# @Description:


import json
from ws4py.client.threadedclient import WebSocketClient
from state import State
from action import Action


class ExampleClient(WebSocketClient):

    def __init__(self, url):
        super().__init__(url)
        self.state = State()
        self.action = Action()
        self.my_pos = -1        # 增加了一个属性，用来记录自己的位置
        self.mate_pos = -1           # 增加了一个属性，用来记录队友的位置

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        message = json.loads(str(message))                                    # 先序列化收到的消息，转为Python中的字典
        self.state.parse(message)
        if message["stage"] == "beginning":   # 先从beginning阶段获取自己的位置
            self.my_pos = message["myPos"]        # 根据自己的位置推断出队友的位置
            self.mate_pos = (self.my_pos+2) % 4

        if "actionList" in message:                                           # 需要做出动作选择时调用动作对象进行解析
            act_index = self.action.parse(message, self.mate_pos)
            # 在action.parse中增加了一个新参数，传入队友的位置

            # act_index = self.action.parse(message, -1)         # 传入-1时默认为“笨笨”操作，不会调用算法
            self.send(json.dumps({"actIndex": act_index}))


if __name__ == '__main__':
    try:
        ws = ExampleClient('ws://192.168.2.121:9618/game/gd/19852273119381168')
        # ws = ExampleClient('ws://112.124.24.226:80/game/gd/19852273119160234')
        # ws = ExampleClient('ws://112.124.24.226:80/game/gd/19852273119160234')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
