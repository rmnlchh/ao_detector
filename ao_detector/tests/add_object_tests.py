import unittest
from unittest.mock import MagicMock, patch
from telegram import Update, Message, User, Contact
from telegram.ext import CallbackContext, Dispatcher

from handler import handle_text_message, handle_unknown_command, help, share, photo


class TestBot(unittest.TestCase):
    def setUp(self):
        self.update = Update(123, message=Message(12350954, None, None, '/start'))
        self.context = CallbackContext(Dispatcher(None, None, None, None))
        self.mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = self.mock_reply_text

    class MockReplyText:
        def __init__(self):
            self.text = ""

        def __call__(self, text, reply_markup=None):
            self.text = text
            self.reply_markup = reply_markup

    @patch('save_new_object_type')
    def test_handle_text_message_add_new_object_correct(self, mock_save_new_object_type):
        self.update.message.text = 'Додати:X11'
        handle_text_message(self.update, self.context)
        mock_save_new_object_type.assert_called_with('X11', self.update, self.context)

    @patch('handle_unknown_command')
    def test_handle_text_message_add_new_object_incorrect(self, mock_handle_unknown_command):
        self.update.message.text = 'Додати'
        handle_text_message(self.update, self.context)
        mock_handle_unknown_command.assert_called_with(self.update, self.context)


if __name__ == '__main__':
    unittest.main()
