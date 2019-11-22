import unittest

from unittest.mock import Mock
from exceptions import NotADM, CampaignNotFound, CharacterNotFound
from decorators import only_dm, get_campaign, get_character

CHAT_ID = '666'
CAMPAIGN_ID = '123456'
CHARACTER_ID = '777'

def dummy_func(command, txt_args, db, chat_id, username, **kargs):
    pass

class TestDecorators(unittest.TestCase):

    def setUp(self):
        self.db = Mock()
        self.campaign = {
            'dm_username': 'foobar'
        }
        self.kargs = {
            'campaign_id': CAMPAIGN_ID,
            'campaign': self.campaign
        }

    def test_only_dm_with_non_dm_user(self):
        # execution
        with self.assertRaises(NotADM) as context:
            only_dm(dummy_func)('', '', self.db, CHAT_ID, 'foo', **self.kargs)

    def test_only_dm_with_valid_user(self):
        # execution
        only_dm(dummy_func)('', '', self.db, CHAT_ID, 'foobar', **self.kargs)

    def test_only_dm_with_empty_campaign(self):
        # conditions
        kargs = self.kargs
        kargs['campaign'] = None

        # execution
        with self.assertRaises(CampaignNotFound) as context:
            only_dm(dummy_func)('', '', self.db, CHAT_ID, 'foobar', **kargs)

    def test_get_campaign_with_empty_campaign(self):
        # conditions
        self.db.get_campaign = Mock(return_value=(None, None))

        # execution
        with self.assertRaises(CampaignNotFound) as context:
            get_campaign(dummy_func)('', '', self.db, CHAT_ID, 'foobar', **{})

    def test_get_campaign_with_valid_campaign(self):
        # conditions
        self.kargs = {}
        self.db.get_campaign = Mock(return_value=(CAMPAIGN_ID, self.campaign))

        # expected
        def assert_func(command, txt_args, db, chat_id, username, **kargs):
            self.assertTrue('campaign' in kargs)
            self.assertTrue('campaign_id' in kargs)
            self.assertEquals(CAMPAIGN_ID, kargs.get('campaign_id'))

        # execution
        get_campaign(dummy_func)('', '', self.db, CHAT_ID, 'foobar', **self.kargs)

    def test_get_character_with_empty_campaign(self):
        # execution
        with self.assertRaises(CampaignNotFound) as context:
            get_character(dummy_func)('', '', self.db, CHAT_ID, 'foobar', **{})

    def test_get_character_with_empty_character(self):
        # conditions
        self.db.get_character_id = Mock(return_value=None)
        self.db.get_character = Mock(return_value=None)

        # execution
        with self.assertRaises(CharacterNotFound) as context:
            get_character(dummy_func)('', '', self.db, CHAT_ID, 'foobar', **self.kargs)

    def test_get_character_with_valid_character(self):
        # conditions
        self.db.get_character_id = Mock(return_value=CHARACTER_ID)
        self.db.get_character = Mock(return_value={'result': True})

        # expected
        def assert_func(command, txt_args, db, chat_id, username, **kargs):
            self.assertTrue('character' in kargs)
            self.assertTrue('character_id' in kargs)
            self.assertEquals(CHARACTER_ID, kargs.get('character_id'))
            self.assertEquals(True, kargs.get('character').get('result'))

        # execution
        get_character(dummy_func)('', '', self.db, CHAT_ID, 'foobar', **self.kargs)
