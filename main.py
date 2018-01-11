from wxpy import *
from random import randrange

def intro(msg):
    global mgr_id, group_id
    ret = list()
    ret.append("你好，我叫{}，正在{}群工作\n".format(mgr_id, group_id))
    ret.append("AT我+命令就可以了(例:@{} intro)".format(mgr_id))
    return ret

def man(msg):
    global mgr_id
    ret = list()
    ret.append("使用方法：@机器人+命令")
    ret.append("例：@{} intro".format(mgr_id))
    return ret

def faq(msg):
    pass

def ques(msg): # question
    global questions
    ret = list()
    number = randrange(0, 10000)
    print("收到提问，分配编号{}".format(number))
    while number in questions:
        number = randrange(0, 10000)

    questions[number] = "unresolved"
    print("开启提问")
    ret.append("问题已分配编号No.{}".format(number))
    ret.append("回答请@{} a {}".format(mgr_id, number))
    print(ret)

    return ret

def answ(msg): # answer
    print("answering" + msg)
    global group
    ret = list()
    number = str(msg[len(group.self.name) + 4:]) # offset for @, space, a and space
    print("No.{}".format(number))
    if number not in questions:
        ret.append("啊哦，问题编号无效，请检查")
    else:
        if questions[number] == "taken":
            ret.append("添加新回答")
        else:
            ret.append("回答No.{}".format(number))
    return ret

def resolved(msg): # resolved
    ret = list()
    number = str(msg[len(group.self.name) + 2:])
    if number not in questions:
        ret.append("啊哦，问题编号无效，请检查")
    else:
        ret.append("问题No.{}已解决，关闭问题".format(number))
        del questions[number]
    return ret

mgr_id = "*pWally"
owner_id = "瓦利一号"
group_id = "HYCLZ"

commands = {
    "intro": intro,
    "man": man,
    "faq": faq,
    "q": ques,
    "a": answ,
    "resolved": resolved}

questions = dict()

mgr = Bot() # create wechat manager
owner = mgr.friends().search(owner_id)[0]
group = mgr.groups().search(group_id)[0]

@mgr.register(owner)
def reply_owner(msg):
    return 'received: {} ({})'.format(msg.text, msg.type)

@mgr.register(group)
def reply_group_message(msg):
    if msg.is_at == True:
        print(msg.text)
        print("_{}_".format(msg.member.display_name))

        command = msg.text[len(group.self.name) + 2:] # offset for @ and space
        print("_{}_".format(command))

        if command in commands:
            # print("command mode")
            ret_msgs = commands[command](msg)
            for ret_msg in ret_msgs:
                group.send(ret_msg)
            return
        elif len(command) > 0 and command[0] == "a":
            print("answer mode")
            ret_msgs = commands[command[0]](msg)
            for ret_msg in ret_msgs:
                group.send(ret_msg)
            return
        else:
            # print("at mode")
            return "我被AT了！"
    else:
        print('received: {} ({})'.format(msg.text, msg.type))

mgr.self.send("Wechat Group Manager Online")
owner.send('{}你好，{}正在工作～'.format(owner_id, mgr_id))
group.send("{}群管理机器人已上线".format(mgr_id))

embed()

