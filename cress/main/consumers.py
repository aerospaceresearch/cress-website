from channels import Group


def ws_add(message):
    Group("all").add(message.reply_channel)


def ws_message(message):
    pass


def ws_disconnect(message):
    Group("all").discard(message.reply_channel)
