import unittest
from unittest.mock import MagicMock, patch
from telegram import Update, Message, User, Contact
from telegram.ext import CallbackContext, Dispatcher

from handler import handle_text_message, handle_unknown_command, help, share, photo


class TestBot(unittest.TestCase):
    def setUp(self):
        self.update = Update(123, message=Message(12350954, None, None, '/start'))
        self.dispatcher = Dispatcher(None, None, None, None)
        self.context = CallbackContext(self.dispatcher)

    class MockReplyText:
        def __init__(self):
            self.text = ""

        def __call__(self, text, reply_markup=None):
            self.text = text
            self.reply_markup = reply_markup

    @patch('analyze_image')
    def test_photo_unauthorized_user(self, mock_analyze_image):
        self.update.effective_user.id = 0
        mock_analyze_image.return_value = None
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        photo(self.update, self.context)
        self.assertEqual(mock_reply_text.text, 'Об’єкт не розпізнано.')

    @patch('analyze_image')
    def test_photo_authorized_user_dji_mavic_jpg(self, mock_analyze_image):
        self.update.effective_user.id = 1
        mock_analyze_image.return_value = {"Confidence": 90, "Name": "Dji mavic"}
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        photo(self.update, self.context)
        self.assertIn('Об’єкт "Dji mavic" виявлено', mock_reply_text.text)

    @patch('analyze_image')
    def test_photo_authorized_user_iskander_jpg(self, mock_analyze_image):
        self.update.effective_user.id = 1
        mock_analyze_image.return_value = {"Confidence": 90, "Name": "Iskander"}
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        photo(self.update, self.context)
        self.assertIn('Об’єкт "Iskander" виявлено', mock_reply_text.text)

    @patch('analyze_image')
    def test_photo_authorized_user_su35_jpg(self, mock_analyze_image):
        self.update.effective_user.id = 1
        mock_analyze_image.return_value = {"Confidence": 90, "Name": "SU-35"}
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        photo(self.update, self.context)
        self.assertIn('Об’єкт "SU-35" виявлено', mock_reply_text.text)

    @patch('analyze_image')
    def test_photo_authorized_user_su27_jpg(self, mock_analyze_image):
        self.update.effective_user.id = 1
        mock_analyze_image.return_value = {"Confidence": 90, "Name": "SU-27"}
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        photo(self.update, self.context)
        self.assertIn('Об’єкт "SU-27" виявлено', mock_reply_text.text)

    @patch('analyze_image')
    def test_photo_authorized_user_su35_png(self, mock_analyze_image):
        self.update.effective_user.id = 1
        mock_analyze_image.return_value = {"Confidence": 90, "Name": "SU-35"}
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        photo(self.update, self.context)
        self.assertIn('Об’єкт "SU-35" виявлено', mock_reply_text.text)

    @patch('analyze_image')
    def test_photo_authorized_user_peony(self, mock_analyze_image):
        self.update.effective_user.id = 1
        mock_analyze_image.return_value = {"Confidence": 90, "Name": "Peony"}
        mock_reply_text = self.MockReplyText()
        self.update.effective_message.reply_text = mock_reply_text
        photo(self.update, self.context)
        self.assertIn('Об’єкт "Peony" виявлено', mock_reply_text.text)


if __name__ == '__main__':
    unittest.main()
