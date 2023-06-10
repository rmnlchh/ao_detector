import unittest
from unittest.mock import MagicMock, patch
from telegram import Update, Message, User
from telegram.ext import CallbackContext, Dispatcher

from handler import handle_text_message, handle_unknown_command, help, start


class TestBot(unittest.TestCase):
    def setUp(self):
        self.update = Update(123, message=Message(12350954, None, None, '/start'))
        self.dispatcher = Dispatcher(None, None, None, None)
        self.context = CallbackContext(self.dispatcher)
        self.start_text_auth = (
            "Ви авторизовані у систему, надішліть зображення для аналізу або перегляньте доступні команди натиснувши 'Допомога' або написавши /help"
        )
        self.start_text_unauth = (
            "Для доступу до повного функціоналу авторизуйтеся у систему або перегляньте доступні команди натиснувши 'Допомога' або написавши /help"
        )

    # Create a mock object for update.effective_message.reply_text
    class MockReplyText:
        def __init__(self):
            self.text = ""

        def __call__(self, text):
            self.text = text

    def test_unauthorized_user_start(self):
        self.update.effective_user.id = 1
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        start(self.update, self.context)
        self.assertEqual(mock_reply_text.text, self.start_text_unauth)

    def test_authorized_user_start(self):
        self.update.effective_user.id = 2
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        start(self.update, self.context)
        self.assertEqual(mock_reply_text.text, self.start_text_auth)

    def test_authorized_user_start_again(self):
        self.update.effective_user.id = 2
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        start(self.update, self.context)
        self.assertEqual(mock_reply_text.text, self.start_text_auth)


if __name__ == '__main__':
    unittest.main()
