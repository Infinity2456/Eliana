import ollama , os , logging , random , threading , time
from telebot import types
from config import TOKEN , model , templat , promt1 , promt2 , cont , rp_mode_switch , eat_switch , magazine_switch # pyright: ignore[reportAttributeAccessIssue]
import telebot
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
bot = telebot.TeleBot(TOKEN)
connect = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\value.db", check_same_thread=False)
cursor_collection = connect.cursor()
connect_ = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\context.db", check_same_thread=False)
cursor_ = connect_.cursor()
logs_number = 0
eat_person = ""
ai = 0


def reset_eat_switch():
    global eat_switch
    eat_switch = 0
    print("eat_switch сброшен в 0")

def reset_magazine_switch():
    global magazine_switch
    magazine_switch = 0
    print("magazine_switch сброшен в 0")

def reset_bank_switch():
    global bank_switch
    bank_switch = 0
    print("bank_switch сброшен в 0")

scheduler = BackgroundScheduler()
scheduler.add_job(reset_eat_switch, 'interval', seconds=1800)
scheduler.add_job(reset_magazine_switch, 'interval', seconds=7200)
scheduler.add_job(reset_bank_switch, 'interval', seconds=14400)
scheduler.start()

def log_number(logs_number):
    if os.path.exists(fr"C:\Users\M4lph4s\Desktop\C#\Logs\{logs_number}.log"):
        logs_number = logs_number + 1
        log_number(logs_number=logs_number)
    else:
        print(f'{logs_number}.logs запись')
        log_dir = os.path.join(os.path.dirname(__file__), 'Logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        logging.basicConfig(filename=os.path.join(log_dir, f'{logs_number}.log'), level=logging.DEBUG,
                            format='%(levelname)s: %(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

log_number(logs_number=logs_number)
## Выдает все описания пользователей
def get_all_opisanie(message):
    conn_opisanie = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\opisanie.db")
    cursor_opisanie = conn_opisanie.cursor()
    cursor_opisanie.execute('SELECT opisanie FROM my_table')
    rows = cursor_opisanie.fetchall()
    row = str(rows)
    row1 = row.replace("',), ('"," ")
    row2 = row1.replace("[('","")
    row3 = row2.replace("',)]","")
    print(row.replace("',), ('"," "))
    conn_opisanie.close()
    return(row3)

## Выдает описание пользователя
def get_opisanie(message):
    conn_opisanie = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\opisanie.db")
    cursor_opisanie = conn_opisanie.cursor()
    cursor_opisanie.execute("SELECT opisanie FROM my_table WHERE id = ?", (message.from_user.id,))
    rows = cursor_opisanie.fetchone()
    conn_opisanie.close()
    return(rows)


## Устанавливает описание пользователя
def set_opisanie(message):
    conn_opisanie = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\opisanie.db")
    cursor_opisanie = conn_opisanie.cursor()
    add = message.text.replace('!сменить описание ','')
    cursor_opisanie.execute("UPDATE my_table SET opisanie = ? WHERE id = ?", (add, message.from_user.id))
    conn_opisanie.commit()
    conn_opisanie.close()
    return()

def get_money(message):
    conn = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT eat_point FROM food_entries WHERE id = ?", (message.from_user.id,))
    rows = cursor.fetchone()
    conn.close()
    return(rows)

def set_money(add,message):
    conn = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\game.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (add, message.from_user.id))
    conn.commit()
    conn.close()
    return()

def set_money_reply(add,message):
    conn = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\game.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (add, message.reply_to_message.from_user.id))
    conn.commit()
    conn.close()
    return()

def get_money_reply(message):
    conn = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT eat_point FROM food_entries WHERE id = ?", (message.reply_to_message.from_user.id,))
    rows = cursor.fetchone()
    conn.close()
    return(rows)

def set_money_0_reply(message):
    conn = sqlite3.connect(fr"C:\Users\M4lph4s\Desktop\C#\game.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (0, message.reply_to_message.from_user.id))
    conn.commit()
    conn.close()
    return()


print("Бот запущен.")

@bot.message_handler(regexp="!Элиана")
def DeepSeek(message):
    if 0 == ai:
        cursor_.execute("SELECT context FROM my_table WHERE id = ?", (1,))
        rows = cursor_.fetchone()
        row3 = get_opisanie(message)
        if 1 == rp_mode_switch:
            if 1 == eat_switch:
                prompt = templat + f'Недавно тебя покормил {eat_person}' + row3 + cont + message.from_user.first_name + promt1 + 'История всех сообщений:' + str(rows[0]) + str(message.text.replace('!Элина', ''))
            else:
                prompt = templat + row3 + cont + message.from_user.first_name + promt1 + 'История всех сообщений:' + str(rows[0]) + str(message.text.replace('!Элина', ''))
        else:
            if 1 == eat_switch:
                prompt = templat + f'Недавно тебя покормил {eat_person}' + row3 + cont + message.from_user.first_name + promt1 + 'История всех сообщений:' + str(rows[0]) + str(message.text.replace('!Элина', ''))
            else:
                prompt = templat + row3 + cont + message.from_user.first_name + promt1 + 'История всех сообщений:' + str(rows[0]) + str(message.text.replace('!Элина', ''))
        print("Думает...")
        bot.send_message(message.chat.id, promt2)
        try:
            result = ollama.generate(model=model, prompt=prompt , think=True , stream=True)
            full_response = ""
            for chunk in result:
                full_response += chunk['response']
                print(chunk['response'], end='', flush=True)
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            full_response = full_response
            bot.send_message(message.chat.id, text=full_response)
            logging.info(f"{message.from_user.first_name} отправил запрос {message} и получил в ответ {full_response}")
        except ollama._types.ResponseError as e: # type: ignore
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            text = '🛑 Внимание проблемы с ИИ сообщите M4lph4s! 🛑'
            logging.error("🛑 Сервера временно не доступны! 🛑")
            bot.send_message(message.chat.id, text)
        print("Ответила.")
        add = str(rows[0]) + f"{message.from_user.first_name}: {message.text.replace("!", '')}" + f"Элиана: {full_response}" # pyright: ignore
        cursor_.execute("UPDATE my_table SET context = ? WHERE id = ?", (add, 1))
        connect_.commit()
    else:
        text = '🛑 Внимание проблемы с ИИ из за этого Элиана уходит в тех.работы! 🛑'
        bot.send_message(message.chat.id, text)


@bot.message_handler(regexp="!delete")
def Delete(message):
    if 5609485310 or 5764338287 == message.from_user.id:
        id_message = int(message.text.replace('!delete ', ''))
        bot.delete_message(chat_id=message.chat.id, message_id=id_message)
        print(f"Удалено сообщение в чате {message.chat.id} от пользователя {message.from_user.first_name}")
    else:
        bot.send_message(message.chat.id, "У вас нет прав на удаление сообщений.")

@bot.message_handler(regexp="!рп")
def rp_switch(message):
    text = ""
    global rp_mode_switch
    if 1 == rp_mode_switch:
        rp_mode_switch = 0
        text = 'Рп режим выключен'
    elif 0 == rp_mode_switch:
        rp_mode_switch = 1
        text = 'Рп режим включен'
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!отключить элиану")
def ai_switch(message):
    if 5609485310 or 5764338287 == message.from_user.id:
        text = ""
        global ai
        if 1 == ai:
            ai = 0
            text = 'Элиана включена'
        elif 0 == ai:
            ai = 1
            text = 'Элиана выключена'
        bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!дать еды")
def eat(message):
    if 0 == ai:
        text = ""
        global eat_switch
        global eat_person
        row3 = get_opisanie(message)
        if 1 == eat_switch:
            prompt = templat + f"Тебя покормили но ты уже наелась а накармил же тебя {message.from_user.first_name}" + row3 + cont + message.from_user.first_name + promt1 + str(message.text.replace('!дать еды', ''))
            bot.send_message(message.chat.id, promt2)
            result = ollama.generate(model=model, prompt=prompt , think=True , stream=True)
            full_response = ""
            for chunk in result:
                full_response += chunk['response']
                print(chunk['response'], end='', flush=True)
            full_response_answer = str(full_response)  + ' (+0 скрепок)'
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
        elif 0 == eat_switch:
            eat_person = f'{message.from_user.first_name}'
            eat_switch = 1
            prompt = templat + f'Тебя накармил {message.from_user.first_name} и ты наелась и довольна' + row3 + cont + message.from_user.first_name + promt1 + str(message.text.replace('!дать еды', ''))
            bot.send_message(message.chat.id, promt2)
            result = ollama.generate(model=model, prompt=prompt , think=True , stream=True)
            full_response = ""
            for chunk in result:
                full_response += chunk['response']
                print(chunk['response'], end='', flush=True)
            full_response_answer = str(full_response) + ' (+10 скрепок)'
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            rows = get_money(message)
            add = int(rows[0]) + 10
            set_money(add,message)
        bot.send_message(message.chat.id, text=full_response_answer) # pyright: ignore
    else:
        text = '(Вы слышите отдоленный голос из пустоты)'
        bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!скрепки")
def eat_ball(message):
    rows = get_money(message)
    if 5 < rows[0]:
        text = f"У вас {rows[0]} скрепок"
    else:
        text = f"У вас {rows[0]} скрепка"
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="<балл управление")
def eat_plus(message):
    if 5609485310 == message.from_user.id:
        if f'<балл управление + {message.text.replace('<балл управление + ','')}' == message.text:
            rows = get_money(message)
            add = int(rows[0]) + int(message.text.replace('<балл управление + ', ''))
            set_money_reply(add,message)
            print('+')
        elif f'<балл управление - {message.text.replace('<балл управление - ', '')}' == message.text:
            rows = get_money(message)
            add = int(rows[0]) - int(message.text.replace('<балл управление - ', ''))
            set_money_reply(add,message)
            print('-')
        elif f'<балл управление = {message.text.replace('<балл управление = ', '')}' == message.text:
            add = int(message.text.replace('<балл управление = ', ''))
            set_money_reply(add,message)
            print('=')
        elif f'<балл управление 0' == message.text:
            set_money_0_reply(message)
            print('0')
        else:
            print('Error')
            print(message.text)
        rows = get_money_reply(message)
        if 5 < rows[0]:
            text = f"У вас {rows[0]} скрепок"
        else:
            text = f"У вас {rows[0]} скрепка"
        bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!казино")
def casino(message):
    rows = get_money(message)
    if 10 <= rows[0]:
        random_values = random.randint(1,2)
        print(random_values)
        if 1 == random_values:
            add = int(rows[0]) + 10
            set_money(add,message)
            text = 'Поздровляю вы выйграли'
        else:
            add = int(rows[0]) - 10
            set_money(add,message)
            text = 'Вы проиграли'
    elif 10 >= rows[0]:
        text = 'Недостаточно скрепок. Ставка: 10 скрепок'
    bot.send_message(message.chat.id, text) # pyright: ignore

@bot.message_handler(regexp="!скрепки передать")
def transit(message):
    rows = get_money(message)
    if rows[0] >= int(message.text.replace('!скрепки передать ', '')):
        ball = rows[0] - int(message.text.replace('!балл передать ', ''))
        set_money(ball,message)
        add = int(message.text.replace('!скрепки передать ', ''))
        set_money_reply(add,message)
        text = f'Успешно передано {message.text.replace('!скрепки передать ', '')} у вас осталось {ball}'
    else:
        text = 'Не хватает'
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!купить скрепки")
def send_payment(message):
    prices = [telebot.types.LabeledPrice(label='Звезда', amount=1)]  # pyright: ignore
    bot.send_invoice(
        message.chat.id,
        title='Покупка скрепок',
        description='1 звезда = 10 скрепок',
        provider_token='',  # Оставьте пустым для оплаты Звёздами
        currency='XTR',     # XTR — валюта Звёзд
        prices=prices,
        start_parameter='test-payment',
        invoice_payload='my_payload_for_internal_use'
    )

@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    payment_info = message.successful_payment
    rows = get_money(message)
    add = int(rows[0]) + 10
    set_money_reply(add,message)
    bot.send_message(
        message.chat.id,
        f'Спасибо за покупку! Вы заплатили {payment_info.total_amount} Звёзд.'
    )

@bot.message_handler(regexp="!купить коллекционку")
def pay_collection(message):
    text = "Вот католог коллекционок"
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("Игрушка 'Портал'. Цена 100", callback_data="btn1")
    btn2 = types.InlineKeyboardButton("Игрушка 'Liable'. Цена 200", callback_data="btn2")
    btn3 = types.InlineKeyboardButton("Игрушка 'Вайбмен'. Цена 700", callback_data="btn3")
    btn4 = types.InlineKeyboardButton("Братец пепси рамшут. Цена 1000", callback_data="btn4")
    markup.add(btn1 , btn2 , btn3 , btn4)
    bot.send_message(message.chat.id, text , reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "btn1":
        ball = get_money(call)
        if 100 <= ball[0]:
            rows = get_money(call)
            add = int(rows[0]) - 100
            set_money(add,call)
            cursor_collection.execute("SELECT value_1 FROM my_table WHERE id = ?", (call.from_user.id,))
            rows1 = cursor_collection.fetchone()
            add1 = int(rows1[0]) + 1
            cursor_collection.execute("UPDATE my_table SET value_1 = ? WHERE id = ?", (add1, call.from_user.id))
            connect.commit()
            bot.answer_callback_query(call.id, "Успешно!")
        else:
            bot.answer_callback_query(call.id, "Недостаточно скрепок!")
    elif call.data == "btn2":
        ball = get_money(call)
        if 200 <= ball[0]:
            rows = get_money(call)
            add = int(rows[0]) - 200
            set_money(add,call)
            cursor_collection.execute("SELECT value_2 FROM my_table WHERE id = ?", (call.from_user.id,))
            rows1 = cursor_collection.fetchone()
            add1 = int(rows1[0]) + 1
            cursor_collection.execute("UPDATE my_table SET value_2 = ? WHERE id = ?", (add1, call.from_user.id))
            connect.commit()
            bot.answer_callback_query(call.id, "Успешно!")
        else:
            bot.answer_callback_query(call.id, "Недостаточно скрепок!")
    elif call.data == "btn3":
        ball = get_money(call)
        if 700 <= ball[0]:
            rows = get_money(call)
            add = int(rows[0]) - 700
            set_money(add,call)
            cursor_collection.execute("SELECT value_3 FROM my_table WHERE id = ?", (call.from_user.id,))
            rows1 = cursor_collection.fetchone()
            add1 = int(rows1[0]) + 1
            cursor_collection.execute("UPDATE my_table SET value_3 = ? WHERE id = ?", (add1, call.from_user.id))
            connect.commit()
            bot.answer_callback_query(call.id, "Успешно!")
        else:
            bot.answer_callback_query(call.id, "Недостаточно скрепок!")
    elif call.data == "btn4":
        ball = get_money(call)
        if 1000 <= ball[0]:
            rows = get_money(call)
            add = int(rows[0]) - 1000
            set_money(add,call)
            cursor_collection.execute("SELECT value_4 FROM my_table WHERE id = ?", (call.from_user.id,))
            rows1 = cursor_collection.fetchone()
            add1 = int(rows1[0]) + 1
            cursor_collection.execute("UPDATE my_table SET value_4 = ? WHERE id = ?", (add1, call.from_user.id))
            connect.commit()
            bot.answer_callback_query(call.id, "Успешно!")
        else:
            bot.answer_callback_query(call.id, "Недостаточно скрепок!")

@bot.message_handler(regexp="!коллекция")
def collection(message):
    cursor_collection.execute("SELECT value_1 FROM my_table WHERE id = ?", (message.from_user.id,))
    rows1 = cursor_collection.fetchone()
    cursor_collection.execute("SELECT value_2 FROM my_table WHERE id = ?", (message.from_user.id,))
    rows2 = cursor_collection.fetchone()
    cursor_collection.execute("SELECT value_3 FROM my_table WHERE id = ?", (message.from_user.id,))
    rows3 = cursor_collection.fetchone()
    cursor_collection.execute("SELECT value_4 FROM my_table WHERE id = ?", (message.from_user.id,))
    rows4 = cursor_collection.fetchone()
    text = f"У вас {str(rows1[0])} Игрушка 'Портал', {str(rows2[0])} Игрушка 'Liable', {str(rows3[0])} Игрушка 'Вайбмен', {str(rows4[0])} Братец пепси рамшут"
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!ограбить магазин")
def magazine(message):
    text = ""
    global magazine_switch
    if 1 == magazine_switch:
        text = 'В магазине пусто.'
    elif 0 == magazine_switch:
        magazine_switch = 1
        text = 'Вы успешно ограбили магазин +50'
        rows = get_money(message)
        add = int(rows[0]) + 50
        set_money(add,message)
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!ограбить банк")
def bank(message):
    text = ""
    global bank_switch
    if 1 == bank_switch:
        text = 'В банке пусто.'
    elif 0 == bank_switch:
        number = random.randint(1, 10)
        number = 12
        bank_switch = 1
        if 2 >= number:
            text = 'Вы успешно ограбили банк +200'
            rows = get_money(message)
            add = int(rows[0]) + 200
            set_money(add,message)
        elif 5 >= number:
            text = 'Вы успешно ограбили банк +100'
            rows = get_money(message)
            add = int(rows[0]) + 100
            set_money(add,message)
        elif 9 >= number:
            text = 'Вы успешно ограбили банк +50'
            rows = get_money(message)
            add = int(rows[0]) + 50
            set_money(add,message)
        else:
            text = 'Вы не смогли ограбить банк и вас поймали! -500 скрепок'
            rows = get_money(message)
            add = int(rows[0]) - 500
            set_money(add,message)
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!отправить")
def send(message):
    if 5609485310 or 5764338287 == message.from_user.id:
        id_message = str(message.text.replace('!отправить ', ''))
        bot.send_message(message.chat.id, id_message)
    else:
        bot.send_message(message.chat.id, "У вас нет прав на отправку сообщений.")

@bot.message_handler(regexp="!сообщение")
def message(message):
    print(message.reply_to_message.from_user.id)

@bot.message_handler(regexp="!описание")
def opisanie(message):
    rows = get_opisanie(message)
    bot.send_message(message.chat.id , text=f"Описание: {rows[0]}")

@bot.message_handler(regexp="!сменить описание")
def sm_opisanie(message):
    set_opisanie(message)
    bot.send_message(message.chat.id , text=f"Описание успешно изменено")


bot.infinity_polling()