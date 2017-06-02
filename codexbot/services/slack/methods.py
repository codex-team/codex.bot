def get_bot_id(slack_client, bot_name):
    members = slack_client.api_call("users.list")
    if members.get('ok'):
        users = members.get('members')
        for user in users:
            if 'name' in user and user.get('name') == bot_name:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
        else:
            print("could not find bot user with the name " + bot_name)


def channels_list(slack_client):
    channels_list = slack_client.api_call("channels.list")
    if channels_list.get('ok'):
        return channels_list['channels']
    return None


def send_message(slack_client, channel_id, message, emoji):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel_id,
        text=message,
        icon_emoji=':' + emoji,
        as_user=True
    )

def channels_info(slack_client, channel_id):
    channel_info = slack_client.api_call("channels.info", channel=channel_id)
    if channel_info:
        return channel_info
    return None