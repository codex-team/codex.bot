import json
import unittest

from codexbot.services.telegram import Telegram
from tests.base import BaseTest


class TelegramTestBase(BaseTest, unittest.TestCase):

    def setUp(self):
        self._telegram = Telegram()

    def testConfiguration(self):
        # Test presence
        from codexbot.services.telegram.config import CALLBACK_ROUTE, BOT_NAME, API_TOKEN, API_URL
        self.assertNotEqual(CALLBACK_ROUTE, "")
        self.assertNotEqual(BOT_NAME, "")
        self.assertNotEqual(API_TOKEN, "")
        self.assertNotEqual(API_URL, "")

        # Test route format
        self.assertEqual(CALLBACK_ROUTE[0], "/")
        self.assertNotEqual(CALLBACK_ROUTE[-1], "/")

    def testSetWebhook(self):
        result = self._telegram.set_webhook()
        self.assertNotEqual(result, False)
        self.is_json(result)
        json_result = json.loads(result)
        self.assertEqual(json_result.get("ok", None), True)
