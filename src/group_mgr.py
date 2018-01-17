from wxpy import *
from random import randrange
import logging


class WechatGroupManager():

    def __init__(self, mgr_id, owner_id, group_id):
        self.mgr_id = mgr_id
        self.mgr = Bot()
        self.owner_id = owner_id
        self.owner = ensure_one(self.mgr.friends().search(owner_id))
        self.group_id = group_id
        self.group = ensure_one(self.mgr.groups().search(group_id))

        self.questions = dict()
        self.commands = {
            "intro": self.intro,
            "man": self.man,
            "faq": self.faq,
            "q": self.ques,
            "a": self.answ,
            "r": self.resolved,
        }

    def get_cmds(self):
        return self.commands

    def run_cmd(self, cmd, args):
        return self.commands[cmd](args)

    def intro(self, args: list):
        logging.info("command received: intro")

        ret = list()
        ret.append("你好，我叫{}，正在{}群工作".format(self.mgr_id, self.group_id))
        ret.append("AT我+命令就可以了(例:@{} intro)".format(self.mgr_id))
        return ret

    def man(self, args: list):
        logging.info("command received: man")

        ret = list()
        ret.append("使用方法：@机器人+命令")
        ret.append("例：@{} intro".format(self.mgr_id))
        return ret

    def faq(self, args: list):
        logging.info("command received: faq")

        ret = list()
        ret.append("Error, command not implemented")
        return ret

    def ques(self, args: list):    # question
        logging.info("command received: ques")

        ret = list()
        number = randrange(0, 10000)
        while number in self.questions:
            number = randrange(0, 10000)
 
        logging.info('assign question with number: {}'.format(number))
        print("收到提问，分配编号{}".format(number))

        self.questions[number] = "unresolved"
        print("开启提问")
        ret.append("问题已分配编号No.{}".format(number))
        ret.append("回答请@{} a {}".format(self.mgr_id, number))
        print(ret)

        return ret

    def answ(self, args: list):    # answer
        logging.info("command received: answ")

        ret = list()
        number = int(args[0])
        print("answering" + str(number))
        print("No.{}".format(number))
        if number not in self.questions:
            logging.info('invalid question number: {}'.format(number))
            ret.append("啊哦，问题编号无效，请检查")
        else:
            if self.questions[number] == "taken":
                logging.info('adding extra answer for question number: {}'.format(number))
                ret.append("添加新回答")
            else:
                logging.info('adding original answer for question number: {}'.format(number))
                ret.append("回答No.{}".format(number))
                self.questions[number] = "taken"
        return ret

    def resolved(self, args: list):    # resolved
        logging.info("command received: resolved")

        ret = list()
        number = int(args[0])
        if number not in self.questions:
            logging.info('invalid question number: {}'.format(number))
            ret.append("啊哦，问题编号无效，请检查")
        else:
            logging.info('question {} resolved, closed'.format(number))
            ret.append("问题No.{}已解决，关闭问题".format(number))
            del self.questions[number]
        return ret
