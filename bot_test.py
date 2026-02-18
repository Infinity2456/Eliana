import telebot , os, ollama , logging , random , sqlite3
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
from config import TOKEN , model , templat , promt1 , promt2 , cont , promt3 , rp_mode_switch , eat_switch , role_chat1 , magazine_switch # pyright: ignore[reportAttributeAccessIssue]
bot = telebot.TeleBot(TOKEN)
logs_number = 0
eat_person = ""
ai = 0

def log_number(logs_number):
    if os.path.exists(fr"/root/C#/Log/{logs_number}.log"):
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

## Выдает все описания пользователей
def get_all_opisanie(message):
    conn_opisanie = sqlite3.connect(fr"/root/C#/opisanie.db")
    cursor_opisanie = conn_opisanie.cursor()
    cursor_opisanie.execute('SELECT opisanie FROM my_table')
    rows = cursor_opisanie.fetchall()
    conn_opisanie.close()
    return(rows[0])

## Выдает описание пользователя
def get_opisanie(message):
    conn_opisanie = sqlite3.connect(fr"/root/C#/opisanie.db")
    cursor_opisanie = conn_opisanie.cursor()
    cursor_opisanie.execute("SELECT opisanie FROM my_table WHERE id = ?", (message.from_user.id,))
    rows = cursor_opisanie.fetchone()
    conn_opisanie.close()
    return(rows[0])


## Устанавливает описание пользователя
def set_opisanie(message , id_message):
    conn_opisanie = sqlite3.connect(fr"/root/C#/opisanie.db")
    cursor_opisanie = conn_opisanie.cursor()
    add = message.text.replace('!сменить описание ','')
    cursor_opisanie.execute("UPDATE my_table SET opisanie = ? WHERE id = ?", (add, id_message))
    conn_opisanie.commit()
    conn_opisanie.close()
    return()

## Выдает количество скрепок пользователя
def get_money(id_message):
    conn = sqlite3.connect(fr"/root/C#/game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT eat_point FROM food_entries WHERE id = ?", (id_message ,))
    rows = cursor.fetchone()
    conn.close()
    return(rows)

## Устанавливает количество скрепок пользователя
def set_money(add,id_message):
    conn = sqlite3.connect(fr"/root/C#/game.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (add, id_message))
    conn.commit()
    conn.close()
    return()

## Устанавливает количество скрепок пользователя
def set_money_reply(add,message):
    conn = sqlite3.connect(fr"/root/C#/game.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (add, message.reply_to_message.from_user.id))
    conn.commit()
    conn.close()
    return()

## Выдает количество скрепок пользователя
def get_money_reply(message):
    conn = sqlite3.connect(fr"/root/C#/game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT eat_point FROM food_entries WHERE id = ?", (message.reply_to_message.from_user.id,))
    rows = cursor.fetchone()
    conn.close()
    return(rows[0])

## Устанавливает количество скрепок пользователя в 0
def set_money_0_reply(message):
    conn = sqlite3.connect(fr"/root/C#/game.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (0, message.reply_to_message.from_user.id))
    conn.commit()
    conn.close()
    return()

## Выдает репутацию пользователя
def get_rep(id_message):
    conn = sqlite3.connect(fr"/root/C#/reputation.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM my_table WHERE id = ?", (id_message,))
    rows = cursor.fetchone()
    conn.close()
    return(rows[0])

## Устанавливает репутацию пользователя
def set_rep(add,id_message):
    conn = sqlite3.connect(fr"/root/C#/reputation.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE my_table SET value = ? WHERE id = ?", (add, id_message))
    conn.commit()
    conn.close()
    return()

def get_vip(id_message):
    conn = sqlite3.connect(fr"/root/C#/vip.db")
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM my_table WHERE id = ?", (id_message,))
    rows = cursor.fetchone()
    conn.close()
    return(rows[0])

def set_vip(add,id_message):
    conn = sqlite3.connect(fr"/root/C#/vip.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE my_table SET value = ? WHERE id = ?", (add, id_message))
    conn.commit()
    conn.close()
    return()



print("Бот запущен.")

@bot.message_handler(regexp="регистрация")
def reg(message):
    connect = sqlite3.connect(fr"/root/C#/value.db", check_same_thread=False)
    cursor_collection = connect.cursor()
    set_money(add=0,id_message=message.from_user.id)
    set_opisanie(message="",id_message=message.from_user.id)
    set_vip(add=0,id_message=message.from_user.id)
    cursor_collection.execute("UPDATE my_table SET value_1 = ? WHERE id = ?", (0,message.from_user.id))
    cursor_collection.execute("UPDATE my_table SET value_2 = ? WHERE id = ?", (0,message.from_user.id))
    cursor_collection.execute("UPDATE my_table SET value_3 = ? WHERE id = ?", (0,message.from_user.id))
    cursor_collection.execute("UPDATE my_table SET value_4 = ? WHERE id = ?", (0,message.from_user.id))
    cursor_collection.execute("UPDATE my_table SET value_5 = ? WHERE id = ?", (0,message.from_user.id))
    connect.commit()
    connect.close()
    text = "Регистрация успешна"
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!Элиана")
def DeepSeek(message):
    if 0 == ai:
        connect_ = sqlite3.connect(fr"/root/C#/context.db", check_same_thread=False)
        cursor_ = connect_.cursor()
        cursor_.execute("SELECT context FROM my_table WHERE id = ?", (1,))
        rows = cursor_.fetchone()
        conn_opisanie = sqlite3.connect(fr"/root/C#/opisanie.db")
        cursor_opisanie = conn_opisanie.cursor()
        cursor_opisanie.execute('SELECT opisanie FROM my_table')
        rows = cursor_opisanie.fetchall()
        row = str(rows)
        row1 = row.replace("',), ('"," ")
        row2 = row1.replace("[('","")
        row3 = row2.replace("',)]","")
        print(row.replace("',), ('"," "))
        if 1 == rp_mode_switch:
            if 1 == eat_switch:
                prompt = templat + f'Недавно тебя покормил {eat_person}' + row3 + cont + message.from_user.first_name + promt1 + 'История всех сообщений в чате:' + str(rows[0]) + str(message.text.replace('!Элина', ''))
            else:
                prompt = templat + row3 + cont + message.from_user.first_name + promt1 + 'История всех сообщений в чате:' + str(rows[0]) + str(message.text.replace('!Элина', ''))
        else:
            if 1 == eat_switch:
                prompt = templat + f'Недавно тебя покормил {eat_person}' + row3 + cont + message.from_user.first_name + promt1 + 'История всех сообщений в чате:' + str(rows[0]) + str(message.text.replace('!Элина', ''))
            else:
                prompt = templat + row3 + cont + message.from_user.first_name + promt1 + 'История всех сообщений в чате:' + str(rows[0]) + str(message.text.replace('!Элина', ''))
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
        connect_.close()
    else:
        text = '🛑 Внимание проблемы с ИИ из за этого Элиана уходит в тех.работы! 🛑'
        bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!delete")
def Delete(message):
    if 5609485310 or 5764338287 == message.from_user.id:
        id_message = int(message.reply_to_message.from_user.id)
        bot.delete_message(message.chat.id, id_message)
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

@bot.message_handler(regexp="!сообщение")
def message(message):
    id_message = message.from_user.id
    print(str(get_money(id_message)))

@bot.message_handler(regexp="!дать еды")
def eat(message):
    conn = sqlite3.connect(fr"/root/C#/game.db", check_same_thread=False)
    cursor = conn.cursor()
    if 0 == ai:
        text = ""
        global eat_switch
        global eat_person
        if 1 == eat_switch:
            prompt = templat + f"Тебя покормили но ты уже наелась а накармил же тебя {message.from_user.first_name}" + role_chat1 + message.from_user.first_name + promt1 + str(message.text.replace('!дать еды', ''))
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
            prompt = templat + f'Тебя накармил {message.from_user.first_name} и ты наелась и довольна' + role_chat1 + message.from_user.first_name + promt1 + str(message.text.replace('!дать еды', ''))
            bot.send_message(message.chat.id, promt2)
            result = ollama.generate(model=model, prompt=prompt , think=True , stream=True)
            full_response = ""
            for chunk in result:
                full_response += chunk['response']
                print(chunk['response'], end='', flush=True)
            full_response_answer = str(full_response) + ' (+10 скрепок)'
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id + 1)
            cursor.execute("SELECT eat_point FROM food_entries WHERE id = ?", (message.from_user.id,))
            rows = cursor.fetchone()
            add = int(rows[0]) + 10
            cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (add, message.from_user.id))
            conn.commit()
        bot.send_message(message.chat.id, text=full_response_answer) # pyright: ignore
    else:
        text = '(Вы слышите отдоленный голос из пустоты)'
        bot.send_message(message.chat.id, text)
    conn.close()

@bot.message_handler(regexp="!скрепки")
def eat_ball(message):
    id_message = message.from_user.id
    rows = get_money(id_message)
    if 5 < rows[0]:
        text = f"У вас {rows[0]} скрепок"
    else:
        text = f"У вас {rows[0]} скрепка"
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!коллекция")
def collection(message):
    connect = sqlite3.connect(fr"/root/C#/value.db", check_same_thread=False)
    cursor_collection = connect.cursor()
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
    connect.close()

@bot.message_handler(regexp="!ограбить магазин")
def magazine(message):
    text = ""
    global magazine_switch
    id_message = message.from_user.id
    if 1 == magazine_switch:
        text = 'В магазине пусто.'
    elif 0 == magazine_switch:
        magazine_switch = 1
        text = 'Вы успешно ограбили магазин +50'
        rows = get_money(id_message)
        add = int(rows[0]) + 50
        set_money(add,id_message)
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!ограбить банк")
def bank(message):
    text = ""
    id_message = message.from_user.id
    global bank_switch
    if 1 == bank_switch:
        text = 'В банке пусто.'
    elif 0 == bank_switch:
        number = random.randint(1, 10)
        number = 12
        bank_switch = 1
        if 2 <= number:
            text = 'Вы успешно ограбили банк +200'
            rows = get_money(id_message)
            add = int(rows[0]) + 200
            set_money(add,id_message)
        elif 5 <= number:
            text = 'Вы успешно ограбили банк +100'
            rows = get_money(id_message)
            add = int(rows[0]) + 100
            set_money(add,id_message)
        elif 9 <= number:
            text = 'Вы успешно ограбили банк +50'
            rows = get_money(id_message)
            add = int(rows[0]) + 50
            set_money(add,id_message)
        else:
            text = 'Вы не смогли ограбить банк и вас поймали! -500 скрепок'
            rows = get_money(id_message)
            add = int(rows[0]) - 500
            set_money(add,id_message)
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!отправить")
def send(message):
    if 5609485310 or 5764338287 == message.from_user.id:
        id_message = str(message.text.replace('!отправить ', ''))
        bot.send_message(message.chat.id, id_message)
    else:
        bot.send_message(message.chat.id, "У вас нет прав на отправку сообщений.")

@bot.message_handler(regexp="!описание")
def opisanie(message):
    conn_opisanie = sqlite3.connect(fr"/root/C#/opisanie.db")
    cursor_opisanie = conn_opisanie.cursor()
    cursor_opisanie.execute("SELECT opisanie FROM my_table WHERE id = ?", (message.from_user.id,))
    rows = cursor_opisanie.fetchone()
    bot.send_message(message.chat.id , text=f"Описание: {rows[0]}")
    conn_opisanie.close()

@bot.message_handler(regexp="!сменить описание")
def sm_opisanie(message):
    conn_opisanie = sqlite3.connect(fr"/root/C#/opisanie.db")
    cursor_opisanie = conn_opisanie.cursor()
    add = message.text.replace('!сменить описание ','')
    cursor_opisanie.execute("UPDATE my_table SET opisanie = ? WHERE id = ?", (add, message.from_user.id))
    conn_opisanie.commit()
    bot.send_message(message.chat.id , text=f"Описание успешно изменено")
    conn_opisanie.close()

@bot.message_handler(regexp="<сменить описание")
def test(message):
    conn_opisanie = sqlite3.connect(fr"/root/C#/opisanie.db")
    cursor_opisanie = conn_opisanie.cursor()
    cursor_opisanie.execute('SELECT opisanie FROM my_table')
    rows = cursor_opisanie.fetchall()
    row = str(rows)
    print(row.replace("',), ('"," "))
    conn_opisanie.close()


@bot.message_handler(regexp="<балл управление")
def eat_plus(message):
    conn = sqlite3.connect(fr"/root/C#/game.db", check_same_thread=False)
    cursor = conn.cursor()
    if 5609485310 == message.from_user.id:
        if f'<балл управление + {message.text.replace('<балл управление + ','')}' == message.text:
            cursor.execute("SELECT eat_point FROM food_entries WHERE id = ?", (message.reply_to_message.from_user.id,))
            rows = cursor.fetchone()
            add = int(rows[0]) + int(message.text.replace('<балл управление + ', ''))
            cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (add, message.reply_to_message.from_user.id))
            conn.commit()
            print('+')
        elif f'<балл управление - {message.text.replace('<балл управление - ', '')}' == message.text:
            cursor.execute("SELECT eat_point FROM food_entries WHERE id = ?", (message.reply_to_message.from_user.id,))
            rows = cursor.fetchone()
            add = int(rows[0]) - int(message.text.replace('<балл управление - ', ''))
            cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (add, message.reply_to_message.from_user.id))
            conn.commit()
            print('-')
        elif f'<балл управление = {message.text.replace('<балл управление = ', '')}' == message.text:
            add = int(message.text.replace('<балл управление = ', ''))
            cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (add, message.reply_to_message.from_user.id))
            conn.commit()
            print('=')
        elif f'<балл управление 0' == message.text:
            cursor.execute("SELECT eat_point FROM food_entries WHERE id = ?", (message.reply_to_message.from_user.id,))
            cursor.execute("UPDATE food_entries SET eat_point = ? WHERE id = ?", (0, message.reply_to_message.from_user.id))
            conn.commit()
            print('0')
        else:
            print('Error')
            print(message.text)
        cursor.execute("SELECT eat_point FROM food_entries WHERE id = ?", (message.reply_to_message.from_user.id,))
        rows = cursor.fetchone()
        if 5 < rows[0]:
            text = f"У вас {rows[0]} скрепок"
        else:
            text = f"У вас {rows[0]} скрепка"
        bot.send_message(message.chat.id, text)
    conn.close()

@bot.message_handler(regexp="!казино")
def casino(message):
    text = ''
    id_message = message.from_user.id
    rows = get_money(id_message)
    if 10 <= rows[0]:
        random_values = random.randint(1,2)
        print(random_values)
        if 1 == random_values:
            add = int(rows[0]) + 10
            set_money(add,id_message)
            text = 'Поздровляю вы выйграли'
        else:
            add = int(rows[0]) - 10
            set_money(add,id_message)
            text = 'Вы проиграли'
    elif 10 >= rows[0]:
        text = 'Недостаточно скрепок. Ставка: 10 скрепок'
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!скрепка передать")
def transit(message):
    id_message = message.from_user.id
    id_reply = message.reply_to_message.from_user.id
    rows = get_money(id_message)
    rows_reply = get_money(id_reply)
    if int(rows[0]) >= int(message.text.replace('!скрепка передать ', '')):
        ball = rows[0] - int(message.text.replace('!скрепка передать ', ''))
        add = rows_reply[0] + int(message.text.replace('!скрепка передать ', ''))
        set_money(ball,id_message)
        set_money(add,id_reply)
        text = f'Успешно передано {message.text.replace('!скрепка передать ', '')} у вас осталось {ball}'
    else:
        text = 'Не хватает'
    bot.send_message(message.chat.id, text)

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


@bot.message_handler(regexp="!панель")
def panel(message):
    if 5609485310 or 5764338287 == message.from_user.id:
        text = "Панель управления ботом"
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("Включить/Выключить Элиану", callback_data="btn_ai")
        btn2 = types.InlineKeyboardButton("Включить/Выключить РП режим", callback_data="btn_rp")
        btn3 = types.InlineKeyboardButton("Узнать баланс всех пользователей", callback_data="btn_ball")
        markup.add(btn1 , btn2, btn3)
        bot.send_message(message.chat.id, text , reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    connect = sqlite3.connect(fr"/root/C#/value.db", check_same_thread=False)
    cursor_collection = connect.cursor()
    id_message = call.from_user.id
    ball = get_money(id_message)
    if call.data == "btn1":
        if 100 <= ball[0]:
            add = int(ball[0]) - 100
            set_money(add,id_message)
            cursor_collection.execute("SELECT value_1 FROM my_table WHERE id = ?", (call.from_user.id,))
            rows1 = cursor_collection.fetchone()
            add1 = int(rows1[0]) + 1
            cursor_collection.execute("UPDATE my_table SET value_1 = ? WHERE id = ?", (add1, call.from_user.id))
            connect.commit()
            bot.answer_callback_query(call.id, "Успешно!")
        else:
            bot.answer_callback_query(call.id, "Недостаточно скрепок!")
    elif call.data == "btn2":
        if 200 <= ball[0]:
            add = int(ball[0]) - 200
            set_money(add,id_message)
            cursor_collection.execute("SELECT value_2 FROM my_table WHERE id = ?", (call.from_user.id,))
            rows1 = cursor_collection.fetchone()
            add1 = int(rows1[0]) + 1
            cursor_collection.execute("UPDATE my_table SET value_2 = ? WHERE id = ?", (add1, call.from_user.id))
            connect.commit()
            bot.answer_callback_query(call.id, "Успешно!")
        else:
            bot.answer_callback_query(call.id, "Недостаточно скрепок!")
    elif call.data == "btn3":
        if 700 <= ball[0]:
            add = int(ball[0]) - 700
            set_money(add,id_message)
            cursor_collection.execute("SELECT value_3 FROM my_table WHERE id = ?", (call.from_user.id,))
            rows1 = cursor_collection.fetchone()
            add1 = int(rows1[0]) + 1
            cursor_collection.execute("UPDATE my_table SET value_3 = ? WHERE id = ?", (add1, call.from_user.id))
            connect.commit()
            bot.answer_callback_query(call.id, "Успешно!")
        else:
            bot.answer_callback_query(call.id, "Недостаточно скрепок!")
    elif call.data == "btn4":
        if 1000 <= ball[0]:
            add = int(ball[0]) - 1000
            set_money(add,id_message)
            cursor_collection.execute("SELECT value_4 FROM my_table WHERE id = ?", (call.from_user.id,))
            rows1 = cursor_collection.fetchone()
            add1 = int(rows1[0]) + 1
            cursor_collection.execute("UPDATE my_table SET value_4 = ? WHERE id = ?", (add1, call.from_user.id))
            connect.commit()
            bot.answer_callback_query(call.id, "Успешно!")
        else:
            bot.answer_callback_query(call.id, "Недостаточно скрепок!")
    elif call.data == "btn_ai":
        global ai
        text = ""
        if 1 == ai:
            ai = 0
            text = 'Элиана включена'
        elif 0 == ai:
            ai = 1
            text = 'Элиана выключена'
        bot.answer_callback_query(call.id, text)
    elif call.data == "btn_rp":
        global rp_mode_switch
        text = ""
        if 1 == rp_mode_switch:
            rp_mode_switch = 0
            text = 'Рп режим выключен'
        elif 0 == rp_mode_switch:
            rp_mode_switch = 1
            text = 'Рп режим включен'
        bot.answer_callback_query(call.id, text)
    elif call.data == "btn_ball":
        connect_ball = sqlite3.connect(fr"/root/C#/game.db", check_same_thread=False)
        cursor_ball = connect_ball.cursor()
        cursor_ball.execute("SELECT id FROM food_entries")
        rows_id = cursor_ball.fetchall()
        text = "Баланс всех пользователей:\n"
        for row in rows_id:
            cursor_ball.execute("SELECT eat_point FROM food_entries WHERE id = ?", (row[0],))
            rows_ball = cursor_ball.fetchone()
            text += f"Пользователь с id {row[0]}: {rows_ball[0]} скрепок\n"
        bot.answer_callback_query(call.id, text)
        connect_ball.close()
    connect.close()

@bot.message_handler(regexp=r"^!-$")
def rep_minus(message):
    target_id = message.reply_to_message.from_user.id
    current = get_rep(target_id)
    set_rep(current - 1, target_id)
    text = f"Вы успешно понизили репутацию пользователя {message.reply_to_message.from_user.first_name} на 1 балл. Текущая репутация: {get_rep(target_id)}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp=r"^!\+$")
def rep_plus(message):
    target_id = message.reply_to_message.from_user.id
    current = get_rep(target_id)
    set_rep(current + 1, target_id)
    text = f"Вы успешно повысили репутацию пользователя {message.reply_to_message.from_user.first_name} на 1 балл. Текущая репутация: {get_rep(target_id)}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!репутация")
def show_rep(message):
    id_message = message.from_user.id
    text = f"Ваша репутация: {get_rep(id_message)}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!репутация пользователя")
def show_rep_user(message):
    if not getattr(message, 'reply_to_message', None) or not getattr(message.reply_to_message, 'from_user', None):
        bot.send_message(message.chat.id, "Команда должна быть ответом на сообщение пользователя.")
        return
    target_id = message.reply_to_message.from_user.id
    text = f"Репутация пользователя {message.reply_to_message.from_user.first_name}: {get_rep(target_id)}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!Мафия")
def mafia(message):
    text = "Игра в мафию скоро будет доступна!"
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!VIP")
def vip(message):
    text = "Список привилегий VIP статуса:\n1. Уникальная роль в чате \n2. Доступ к эксклюзивным стикерам\n3. Приоритет в поддержке\n4. Ранний доступ к новым функциям бота\n5.Ежемесячные бонусы в виде скрепок"
    id_message = message.from_user.id
    value_vip = get_vip(id_message)
    if value_vip == 1:
        text += "\n\nВы являетесь VIP пользователем!"
    else:
        text += "\n\nУ вас нет VIP статуса. Чтобы приобрести VIP статус, пропишите !купить VIP."
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp="!купить VIP")
def buy_vip(message):
    text = ""
    id_message = message.from_user.id
    rows = get_money(id_message)
    if 500 <= rows[0]:
        add = int(rows[0]) - 500
        set_money(add,id_message)
        set_vip(add=1,id_message=id_message)
        text = "Поздравляю вы приобрели VIP статус!"
    else:
        text = "Недостаточно скрепок. Цена VIP статуса: 500 скрепок."
    bot.send_message(message.chat.id, text)

@bot.message_handler(regexp='!я ')
def kto(message):
    reqeust = str(message.text.replace('!я ',""))
    random_namber = random.randint(1,100)
    text = "Ты " + reqeust + " на " + str(random_namber) + "%."
    bot.send_message(message.chat.id, text)

bot.infinity_polling()
