from wxpy import *
from group_mgr import WechatGroupManager
import logging


def reply_owner(msg: Message):
    global manager
    return 'received: {} ({})'.format(msg.text, msg.type)


def reply_group_message(msg: Message):
    global manager
    # commands = manager.commands
    if msg.is_at:
        logging.info('received behavior: {} ({})'.format(msg.text, msg.type))

        args = msg.text.split()
        if len(args) <= 1:
            logging.info('AT without command')
            return "我被AT了！"
        elif args[1] not in manager.get_cmds():
            logging.info('invalid command received: {}'.format(args[1]))
            return "Error: command not found"
        else:
            logging.info('commands received: {}'.format(args[1]))
            ret_msgs = manager.run_cmd(args[1], args[2:])
            for ret_msg in ret_msgs:
                msg.reply(ret_msg)
            return None
    else:
        logging.info('received: {} ({})'.format(msg.text, msg.type))


if __name__ == '__main__':
    global manager

    logging.basicConfig(level=logging.INFO)

    mgr_id = "*pWally"
    owner_id = "瓦利一号"
    group_id = "Bot Test Group"

    manager = WechatGroupManager(mgr_id, owner_id, group_id)

    group_msg_decorator = manager.mgr.register(manager.group)
    group_msg_decorator(reply_group_message)

    owner_msg_decorator = manager.mgr.register(manager.owner)
    owner_msg_decorator(reply_owner)

    manager.mgr.self.send("Wechat Group Manager Online")
    manager.owner.send('{}你好，{}正在工作～'.format(owner_id, mgr_id))
    manager.group.send("{}群管理机器人已上线".format(mgr_id))

    embed()    # blocked and Python repl
    # mgr.join()     # blocked only
