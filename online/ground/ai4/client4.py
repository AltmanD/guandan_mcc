# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 16:30
# @Author     : Duofeng Wu
# @File       : client.py
# @Description:


import json
from ws4py.client.threadedclient import WebSocketClient
from state import State
from action import Action


class ExampleClient(WebSocketClient):

    def __init__(self, url):
        super().__init__(url)
        self.state = State("client4")
        self.action = Action("client4")

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        message = json.loads(str(message))                                    # 先序列化收到的消息，转为Python中的字典
        self.state.parse(message)                                             # 调用状态对象来解析状态
        if "actionList" in message:
            # act_index = self.action.random_parse(message)# 需要做出动作选择时调用动作对象进行解析
            act_index = self.action.rule_parse(message,self.state._myPos,self.state.remain_cards,self.state.history,
                                               self.state.remain_cards_classbynum,self.state.pass_num,
                                               self.state.my_pass_num,self.state.tribute_result)
            self.send(json.dumps({"actIndex": act_index}))


if __name__ == '__main__':
    try:
        #ws = ExampleClient('ws://114.55.107.187:9618/game/gd/client3')
        ws = ExampleClient('ws://127.0.0.1:9618/game/gd/client4')
        # ws = ExampleClient('ws://127.0.0.1:9618/game/gd/13913359464588075')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
