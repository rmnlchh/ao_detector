from io import BytesIO

from telegram import KeyboardButton, ReplyKeyboardMarkup

from database import is_user_authorized, add_user
from rekognition import analyze_image, add_to_dataset, get_latest_file, read_obj_to_bytes
from utils import is_valid_phone_number, map_object_type_to_name, generate_object_type_keyboard, get_object_names, \
    test_bucket, get_key_by_value


def start(update, context):
    user_id = update.effective_user.id

    if is_user_authorized(user_id):
        keyboard = [[KeyboardButton('Допомога')]]
        update.message.reply_text(
            text="Ви авторизовані у систему, надішліть зображення для аналізу або перегляньте доступні команди натиснувши 'Допомога' або написавши /help",
            reply_markup=ReplyKeyboardMarkup(keyboard))
    else:
        keyboard = [[KeyboardButton('Поділитися', request_contact=True), KeyboardButton('Допомога')]]
        update.message.reply_text(
            text="Для доступу до повного функціоналу авторизуйтеся у систему або перегляньте доступні команди натиснувши 'Допомога' або написавши /help",
            reply_markup=ReplyKeyboardMarkup(keyboard))


def help(update, context):
    if not is_user_authorized(update.effective_user.id):
        keyboard = [[KeyboardButton('Поділитися', request_contact=True), KeyboardButton('Допомога')]]
        update.message.reply_text(
            "Привіт! Я - бот, що допомагає з аналізом зображень. На даний момент ви не авторизовані. \n\n"
            "Доступні команди: \n"
            "/start - Розпочати діалог \n"
            "/help - Отримати це повідомлення довідки \n"
            "Поділитися - Авторизуватися в системі, надіславши свій номер телефону. \n\n"
            "Будь ласка, натисніть 'Поділитися', щоб авторизуватися і отримати доступ до всіх можливостей бота."
            , reply_markup=ReplyKeyboardMarkup(keyboard)
        )
    else:
        update.message.reply_text(
            "Привіт! Я - бот, що допомагає з аналізом зображень. Ви авторизовані та маєте доступ до всіх можливостей бота. \n\n"
            "Доступні команди: \n"
            "/start - Розпочати діалог \n"
            "/help - Отримати це повідомлення довідки \n"
            "Надіслати Зображення - Отримати аналіз зображення \n"
            "Додати новий об'єкт - Додати новий об'єкт для аналізу \n\n"
            "Просто надішліть мені зображення, і я намагатимусь його аналізувати!"
        )


def share(update, context):
    contact = update.message.contact
    if contact:
        phone_number = contact.phone_number
        # validation to ensure the phone number is valid and is a Ukrainian number.
        print(phone_number)
        if not is_valid_phone_number(phone_number):
            update.message.reply_text(
                "Наразі функціонал боту доступний тільки користувачам з українським номером телефону.")
            return
        user_id = update.effective_user.id
        if is_user_authorized(user_id):
            update.message.reply_text(
                text="Ви авторизовані у систему, надішліть зображення для аналізу або перегляньте доступні команди натиснувши 'Допомога' або написавши /help")
        else:
            add_user(user_id, phone_number)
            keyboard = [[KeyboardButton('Допомога')]]
            update.message.reply_text(
                text="Ви успішно авторизовані! Надішліть зображення для аналізу або перегляньте доступні команди натиснувши 'Допомога' або написавши /help",
                reply_markup=ReplyKeyboardMarkup(keyboard))


def photo(update, context):
    user_id = update.effective_user.id

    # get photo file
    photo_file = update.message.photo[-1].get_file()

    # handle the response
    highest_confidence_label = analyze_image(user_id, photo_file)
    if highest_confidence_label is None:
        keyboard = [[KeyboardButton('Допомога')]]
        update.message.reply_text('Об’єкт не розпізнано.', reply_markup=ReplyKeyboardMarkup(keyboard))
    else:
        confidence = highest_confidence_label['Confidence']
        object_type = highest_confidence_label["Name"]
        object_name = map_object_type_to_name(object_type)
        if 50 <= confidence < 95:
            keyboard = [
                [KeyboardButton('Додати новий об’єкт'), KeyboardButton('Вказати тип'), KeyboardButton('Допомога')]]
            update.message.reply_text(
                f'Об’єкт "{object_name}" виявлено з вірогідністю {confidence:.2f}%. '
                'Якщо ви вважаєте що це не вірно, ви можете вказати правильний тип або додати новий об’єкт.',
                reply_markup=ReplyKeyboardMarkup(keyboard)
            )
        else:
            keyboard = [[KeyboardButton('Допомога')]]
            update.message.reply_text(
                f'Об’єкт "{object_name}" виявлено з вірогідністю {confidence:.2f}%.'
                , reply_markup=ReplyKeyboardMarkup(keyboard))
            add_to_dataset(user_id, object_type)


def add_new_object_type(update, context):
    keyboard = [[KeyboardButton('Допомога')]]

    update.message.reply_text('Вкажіть новий тип обʼєкту у форматі Додати:<тип>.\nДо прикладу "Додати:Х11"'
                              , reply_markup=ReplyKeyboardMarkup(keyboard))


def save_new_object_type(new_type, update, context):
    user_id = update.effective_user.id
    file_prefix = get_latest_file(test_bucket, f'{user_id}/')
    photo = read_obj_to_bytes(test_bucket, file_prefix)

    # send photo to admin along with new_type
    context.bot.send_photo(chat_id='562101602', photo=photo,
                           caption=f'Користувач {user_id} пропонує додати новий тип обʼєктів {new_type}')


def specify_correct_object_type(update, context):
    reply_markup = generate_object_type_keyboard()
    update.message.reply_text('Оберіть коректний тип обʼєкту:', reply_markup=reply_markup)


def add_corrected_object(update, context):
    keyboard = [[KeyboardButton('Допомога')]]
    user_id = update.effective_user.id
    query = update.callback_query
    button_text = query.data

    add_to_dataset(user_id, button_text)
    context.bot.send_message(chat_id=query.message.chat_id, text='Виправлений обʼєкт було успішно додано до датасету',
                             reply_markup=ReplyKeyboardMarkup(keyboard))
    # Delete the message with the buttons
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    query.answer()


def handle_text_message(update, context):
    text = update.message.text
    if text == "Допомога":
        help(update, context)
    elif text == "Вказати тип":
        specify_correct_object_type(update, context)
    elif text == "Додати новий об’єкт":
        add_new_object_type(update, context)
    elif text.startswith('Додати:'):
        save_new_object_type(text.replace('Додати:', ''), update, context)
    else:
        handle_unknown_command(update, context)


def handle_unknown_command(update, context):
    if update.message.text.startswith('/'):
        update.message.reply_text(
            "Нерозпізнана команда, список доступних команд можна переглянути надіславши /help або натиснувши на кнопку 'Допомога'")
