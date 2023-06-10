import unittest
from unittest.mock import MagicMock, patch
from telegram import Update, Message, User
from telegram.ext import CallbackContext, Dispatcher

from handler import handle_text_message, handle_unknown_command, help


class UnknownTests(unittest.TestCase):

    def setUp(self):
        message = MagicMock(spec=Message)
        message.from_user = MagicMock(spec=User)
        message.from_user.id = 123
        message.text = ''
        self.update = MagicMock(spec=Update)
        self.update.message = message
        self.context = MagicMock(spec=CallbackContext)
        self.context.args = []

    def test_unknown_command(self):
        self.update.message.text = '/abc'
        handle_text_message(self.update, self.context)
        self.update.message.reply_text.assert_called_once_with(
            "Нерозпізнана команда, список доступних команд можна переглянути надіславши /help або натиснувши на кнопку 'Допомога'")


if __name__ == "__main__":
    unittest.main()
