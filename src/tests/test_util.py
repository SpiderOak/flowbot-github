from unittest import TestCase
from .. import util


class TestUtil(TestCase):
    """Test the utility functions."""

    def test_traverse_path(self):
        """Make sure our dict traversal method works as expected."""
        data = {
            'hello': {
                'world': {
                    'foo': 'bar'
                }
            }
        }
        path = ['hello', 'world', 'foo']
        result = util.traverse_dict(data, path)
        self.assertEqual(result, 'bar')

    def test_get_usernames(self):
        """Assert that _get_usernames traverses a data object correctly."""
        data = {
            'issue': {
                'user': {
                    'login': 'foouser'
                }
            },
            'repository': {
                'owner': {
                    'login': 'repoowner'
                }
            },
            'assignee': {
                'login': 'assigneeuser'
            },
            'sender': {
                'login': 'senderuser'
            }
        }

        userpaths = (
            ['issue', 'user'],
            ['repository', 'owner'],
            ['assignee'],
            ['sender']
        )

        usernames = util.get_usernames(data, userpaths)
        expected = set(['foouser', 'repoowner', 'assigneeuser', 'senderuser'])
        self.assertEqual(expected, usernames)

    def test_get_usernames_partial(self):
        """Traverse a partial data dict for usernames."""
        data = {
            'issue': {
                'user': {
                    'login': 'foouser'
                }
            }
        }

        userpaths = (
            ['issue', 'user'],
            ['repository', 'owner'],
            ['assignee'],
            ['sender']
        )

        usernames = util.get_usernames(data, userpaths)
        expected = set(['foouser'])
        self.assertEqual(expected, usernames)

    def test_emoji(self):
        """Make sure each of the given actions produces an emoji."""
        emoji_actions = [
            'opened', 'edited', 'merged', 'closed', 'assigned', 'reopened'
        ]
        for action in emoji_actions:
            emoji = util.action_emoji(action)
            self.assertNotEqual(emoji, '')
