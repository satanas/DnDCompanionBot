import unittest

from unittest.mock import Mock
from decorators import only_dm
from exceptions import NotADM, CampaignNotFound


class TestDecorators(unittest.TestCase):

    def setUp(self):
        self.db = Mock()
        campaign = {
            'dm_username': 'foobar'
        }
        self.kargs = {
            'campaign_id': 123456,
            'campaign': campaign
        }


    def test_only_dm_with_non_dm_user(self):
        def test_func(command, txt_args, db, chat_id, username, **kargs):
            pass
        with self.assertRaises(NotADM) as context:
            only_dm(test_func)('', '', self.db, '666', 'foo', **self.kargs)

    def test_only_dm_with_valid_user(self):
        def test_func(command, txt_args, db, chat_id, username, **kargs):
            pass

        only_dm(test_func)('', '', self.db, '666', 'foobar', **self.kargs)

    def test_only_dm_with_empty_campaign(self):
        kargs = self.kargs
        kargs['campaign'] = None
        def test_func(command, txt_args, db, chat_id, username, **kargs):
            pass

        with self.assertRaises(CampaignNotFound) as context:
            only_dm(test_func)('', '', self.db, '666', 'foobar', **self.kargs)
