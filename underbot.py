import types

import telebot
from telebot import types

TOKEN = ""

bot = telebot.TeleBot(TOKEN)

bot.set_my_commands([
    telebot.types.BotCommand("start", "Начать тест")
])

questions = [
    {"text": "Вопрос 1. Что такое андеррайтинг?", "choices": ["a. Процесс оценки рисков и принятия решений о предоставлении кредитов", "b. Процесс подготовки финансовых отчетов", "c. Этап разработки нового финансового продукта"], "correct": 0},
    {"text": "Вопрос 2. Какую основную задачу выполняет андеррайтер?", "choices": ["a. Оформляет страховые полисы", "b. Оценивает благонадежность", "c. Разрабатывает финансовые страгетии для клиентов"], "correct": 1},
    {"text": "Вопрос 3. Как узнать этажность здания, если есть его точный адрес?", "choices": ["a. Позвонить в справочную службу", "b. Используя инструмент Панорама улиц на Яндекс картах или Google maps", "c. Это сделать невозможно"], "correct": 1},
    {"text": "Вопрос 4. Какой из этих факторов НЕ учитывается при анализе заявки на кредит?", "choices": ["a. Кредитная история", "b. Доход заемщика", "c. Цвет глаз заемщика"], "correct": 2},
    {"text": "Вопрос 5. Как ты относишься к работе, связанной с анализом информации?", "choices": ["a. Очень люблю, это моя стихия", "b. Вполне нормально, но не всегда интересно", "c. Предпочитаю избегать работу, где требуется аналитика"], "correct": 0},
    {"text": "Вопрос 6. Как ты оцениваешь свою внимательность к деталям?", "choices": ["a. Я не очень внимателен", "b. Я очень внимателен к деталям и не пропускаю мелочи", "c. Я часто пропускаю важные детали"], "correct": 1},
    {"text": "Вопрос 7. Что тебе было бы наиболее интересно?", "choices": ["a. Найти иголку в стоге сена", "b. Размышлять о бесконечности вселенной", "c. Ловить вайб"], "correct": 0},
    {"text": "Вопрос 8. Как ты относишься к многозадачности?", "choices": ["a. Чувствую волнение, но стараюсь сохранять спокойствие", "b. Нервничаю и могу потерять контроль", "c. Спокойно, распределяю задачи по приоритетам"], "correct": 2},
    {"text": "Вопрос 9. Как ты справляешься с высокими требованиями в учебе/работе?", "choices": ["a. Управляю временем и строю четкий план", "b. Стараюсь учиться/работать усердно, но иногда чувствую себя перегруженным", "c. Чувствую большое давление и испытываю стресс"], "correct": 0},
    {"text": "Вопрос 10. Оцени свои навыки коммуникации с другими людьми.", "choices": ["a. Часто общаюсь, но предпочитаю переписку в мессенджерах", "b. Я люблю живое общение с людьми, это точно моё", "c. Общаюсь не часто, только по очень важным вопросам"], "correct": 1},
]

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {'score': 0, "current_questions": 0}
    print(user_data)
    bot.send_message(message.chat.id, "Добрый день! Пройди предложенный тест и узнай КТО ТЫ!")
    ask_question(message)

def ask_question(message):
    user_id = message.from_user.id
    data = user_data[user_id]
    questions_index = data["current_questions"]

    if questions_index >= len(questions):
        return end_test(message)

    question = questions[questions_index]

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for choice in question['choices']:
        markup.add(choice)

    bot.send_message(message.chat.id, question["text"], reply_markup=markup)

@bot.message_handler(func=lambda message: message.from_user.id in user_data)
def handle_answer(message):
    user_id = message.from_user.id
    data = user_data[user_id]
    questions_index = data["current_questions"]
    question = questions[questions_index]
    user_answer = message.text
    correct_answer = question["choices"][question["correct"]]

    if user_answer == correct_answer:
        data["score"] += 1

    data["current_questions"] += 1
    ask_question(message)




def end_test(message):
    user_id = message.from_user.id
    score = user_data[user_id]["score"]
    del user_data[user_id]

    if score >=8:
        result = "Спасибо за ответы! Можно сделать вывод, что ты - потенциальный андеррайтер!"
    elif score >= 5:
        result = "Спасибо за ответы! Можно сделать вывод, что у тебя явный талант к андеррайтингу!"
    else:
        result = "Спасибо за ответы! У тебя есть способности к андеррайтингу, но их нужно немного прокачать!"

    markup = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, f"{result}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
