import unittest
from unittest.mock import MagicMock, patch
from telegram import Update, Message, User
from telegram.ext import CallbackContext, Dispatcher

from handler import handle_text_message, handle_unknown_command, help


class TestBot(unittest.TestCase):
    def setUp(self):
        self.update = Update(123, message=Message(12350954, None, None, '/help'))
        self.dispatcher = Dispatcher(None, None, None, None)
        self.context = CallbackContext(self.dispatcher)
        self.help_text = (
            "/start - Розпочати діалог \n"
            "/help - Отримати це повідомлення довідки \n"
            "Поділитися - Авторизуватися в системі, надіславши свій номер телефону. \n\n"
            "Будь ласка, натисніть 'Поділитися', щоб авторизуватися і отримати доступ до всіх можливостей бота."
        )

    # Create a mock object for update.effective_message.reply_text
    class MockReplyText:
        def __init__(self):
            self.text = ""

        def __call__(self, text):
            self.text = text

    def test_unauthorized_user_help(self):
        self.update.effective_user.id = 1
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        help(self.update, self.context)
        self.assertEqual(mock_reply_text.text, self.help_text)

    def test_authorized_user_help(self):
        self.update.effective_user.id = 2
        self.help_text = (
            "Привіт! Я - бот, що допомагає з аналізом зображень. Ви авторизовані та маєте доступ до всіх можливостей бота. \n\n"
            "Доступні команди: \n"
            "/start - Розпочати діалог \n"
            "/help - Отримати це повідомлення довідки \n"
            "Надіслати Зображення - Отримати аналіз зображення \n"
            "Додати новий об'єкт - Додати новий об'єкт для аналізу \n\n"
            "Просто надішліть мені зображення, і я намагатимусь його аналізувати!"
        )
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        help(self.update, self.context)
        self.assertEqual(mock_reply_text.text, self.help_text)


if __name__ == '__main__':
    unittest.main()
