import unittest
from unittest.mock import MagicMock, patch
from telegram import Update, Message, User, Contact
from telegram.ext import CallbackContext, Dispatcher

from handler import handle_text_message, handle_unknown_command, help, share


class TestBot(unittest.TestCase):
    def setUp(self):
        self.update = Update(123, message=Message(12350954, None, None, '/start'))
        self.dispatcher = Dispatcher(None, None, None, None)
        self.context = CallbackContext(self.dispatcher)
        self.share_text_auth = (
            "Ви авторизовані у систему, надішліть зображення для аналізу або перегляньте доступні команди натиснувши 'Допомога' або написавши /help"
        )
        self.share_text_unauth = (
            "Ви успішно авторизовані! Надішліть зображення для аналізу або перегляньте доступні команди натиснувши 'Допомога' або написавши /help"
        )
        self.invalid_number_text = (
            "Наразі функціонал боту доступний тільки користувачам з українським номером телефону."
        )

    class MockReplyText:
        def __init__(self):
            self.text = ""

        def __call__(self, text):
            self.text = text

    def test_share_with_ukrainian_phone_number(self):
        self.update.effective_user.id = 1
        self.update.message.contact = Contact(user_id=1, phone_number="380123456789")
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        share(self.update, self.context)
        self.assertEqual(mock_reply_text.text, self.share_text_auth)

    def test_share_with_foreign_phone_number(self):
        self.update.effective_user.id = 2
        self.update.message.contact = Contact(user_id=2, phone_number="19876543210")
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        share(self.update, self.context)
        self.assertEqual(mock_reply_text.text, self.invalid_number_text)


if __name__ == '__main__':
    unittest.main()
