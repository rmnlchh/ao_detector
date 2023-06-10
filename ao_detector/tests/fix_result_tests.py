import unittest
from unittest.mock import MagicMock, patch
from telegram import Update, Message, User, Contact, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext, Dispatcher

from handler import handle_text_message, handle_unknown_command, help, share, photo, add_corrected_object


class TestBot(unittest.TestCase):
    def setUp(self):
        self.update = Update(123, message=Message(12350954, None, None, '/start'))
        self.context = CallbackContext(Dispatcher(None, None, None, None))
        self.mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = self.mock_reply_text
        self.update.callback_query = CallbackQuery(12350955, self.update.effective_message, 'chosen_object_type')

    class MockReplyText:
        def __init__(self):
            self.text = ""

        def __call__(self, text, reply_markup=None):
            self.text = text
            self.reply_markup = reply_markup

    @patch('add_to_dataset')
    @patch('telegram.Bot.delete_message')
    @patch('telegram.Bot.send_message')
    def test_add_corrected_object(self, mock_send_message, mock_delete_message, mock_add_to_dataset):
        user_id = self.update.effective_user.id
        add_corrected_object(self.update, self.context)
        mock_add_to_dataset.assert_called_with(user_id, 'chosen_object_type')
        mock_delete_message.assert_called_with(chat_id=self.update.callback_query.message.chat_id,
                                               message_id=self.update.callback_query.message.message_id)
        mock_send_message.assert_called_with(chat_id=self.update.callback_query.message.chat_id,
                                             text='Виправлений обʼєкт було успішно додано до датасету',
                                             reply_markup=ReplyKeyboardMarkup([[KeyboardButton('Допомога')]]))


if __name__ == '__main__':
    unittest.main()
