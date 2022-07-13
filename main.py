import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from functions import search_users, get_photo, json_create
from db_vk import engine, Session, vk.messages.send, register_user, add_user_photos, check_db_master



#vk_api
vk_session = vk_api.VkApi(token = token group)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


#DB
session = Session()
connection = engine.connect()



def bot():
    for this_event in longpoll.listen():
        if this_event.type == VkEventType.MESSAGE_NEW:
            if this_event.to_me:
                message_text = this_event.text
                return message_text, this_event.user_id


def menu_bot(id_num):
    vk.messages.send(id_num,
              f"ПРИВЕТ\n"
              f"\nПройдите регистрацию.\n"
              f"Для регистрации введите - ДА.\n"
              f"\nУже зарегистрированны?! - начинайте поиск!\n"
              f"Для поиска - девушка 18-25, Екатеринбург\n")


def info():
    vk.messages.send(user_id, f'Это была последняя анкета((.'
                       f'Поиск - девушка 18 - 35 Москва'
                       f'Меню бота - Vkinder')


def reg_new_user(id_num):
    vk.messages.send(id_num, 'Вы прошли регистрацию.')
    vk.messages.send(id_num,
              f"Vkinder - АКТИВАЦИЯ\n")
    register_user(id_num)


if __name__ == '__main__':
    while True:
        msg_text, user_id = bot()
        if msg_text == "Vkinder":
            menu_bot(user_id)
            msg_text, user_id = bot()
            if msg_text.lower() == 'да':
                reg_new_user(user_id)
            elif len(msg_text) > 1:
                sex = 0
                if msg_text[0:7].lower() =='девушка':
                    sex = 1
                elif msg_text[0:7].lower() == 'мужчина':
                    sex = 2
                age_at = msg_text[8:10]
                if int(age_at) < 18:
                   vk.messages.send(user_id, 'Минимальный возраст - 18 лет.')
                    age_at = 18
                age_to = msg_text[11:14]
                if int(age_to) >= 100:
                    vk.messages.send(user_id, 'Максимальное значение 99 лет.')
                    age_to = 99
                city = msg_text[14:len(msg_text)].lower()
                result = search_users(sex, int(age_at), int(age_to), city)
                json_create(result)
                current_user_id = check_db_master(user_id)

                user_photo = get_photo(result[i][3])
                if user_photo == 'нет доступа к фото':
                    continue

                vk.messages.send(user_id, '0 - Далее, \nq - выход из поиска')
                msg_text, user_id = bot()
                if msg_text == '0':
                    if i >= len(result) - 1:
                        info()
                        break
                    # Пробуем добавить анкету в БД
                    try:
                        register_user(user_id, result[i][3], result[i][1],
                                 result[i][0], city, result[i][2], current_user_id.id)

                    except AttributeError:
                        vk.messages.send(user_id, 'Вы не зарегистрировались!\n Введите Vkinder для перезагрузки бота')
                        break

                elif msg_text.lower() == 'q':
                    vk.messages.send(user_id, 'Введите Vkinder для активации бота')
                    break

