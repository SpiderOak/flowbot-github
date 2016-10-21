"""util.py - Utility functions for webhook consumption."""
import emoji


def get_usernames(payload, user_paths):
    """Get a set of usernames from known paths to user objects."""
    usernames = set()
    for user_path in user_paths:
        user = traverse_dict(payload, user_path)
        if user and 'login' in user:
            usernames.add(user.get('login'))
    return usernames


def get_repo_name(payload, repo_path):
    """Return the name of the repo based on repo_path and webhook payload."""
    repo = traverse_dict(payload, repo_path)
    if repo:
        return repo.get('full_name')


def traverse_dict(data, path):
    """Traverse the data-dict and return the value of the last key in path."""
    while len(path) > 0 and data:
        key = path.pop(0)
        data = data.get(key)
    return data


def action_emoji(action):
    """Return appropriate emoji based on the action given."""
    emoji_map = {
        'opened': ':eight_spoked_asterisk:',
        'edited': ':pencil2:',
        'merged': ':white_check_mark:',
        'closed': ':x:',
        'assigned': ':bust_in_silhouette:',
        'reopened': ':recycle:'
    }

    if action in emoji_map:
        alias = emoji_map[action]
        return emoji.emojize(alias, use_aliases=True)
    return ''
