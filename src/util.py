"""util.py - Utility functions for webhook consumption."""


def get_usernames(webhook_data, userpaths):
    """Get a set of usernames from known paths to user objects."""
    usernames = set()
    for userpath in userpaths:
        user = traverse_dict(webhook_data, userpath)
        if user and 'login' in user:
            usernames.add(user.get('login'))
    return usernames


def traverse_dict(data, path):
    """Traverse the data-dict and return the value of the last key in path."""
    while len(path) > 0 and data:
        key = path.pop(0)
        data = data.get(key)
    return data
