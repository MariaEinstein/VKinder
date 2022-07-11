import vk_api
import json
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.exceptions import ApiError
from db_vk import engine, Base, Session, User, Photos
from sqlalchemy.exc import IntegrityError, InvalidRequestError


#vk_api
vk_session = vk_api.VkApi(token = 'token group')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()



#DB
session = Session()
connection = engine.connect()

#search

def search_users(sex, age_at, age_to, city):
    all_persons = []
    link_profile = 'https://vk.com/id'
    vk_ = vk_api.VkApi(token=user_token)
    response = vk_.method('users.search',
                          {'sort': 1,
                           'sex': sex,
                           'status': 1,
                           'age_from': age_at,
                           'age_to': age_to,
                           'has_photo': 1,
                           'count': 25,
                           'online': 1,
                           'hometown': city
                           })
    for element in response['items']:
        person = [
            element['first_name'],
            element['last_name'],
            link_profile + str(element['id']),
            element['id']
        ]
        all_persons.append(person)
    return all_persons


#photo
def get_photo(user_owner_id):
    vk_ = vk_api.VkApi(token=user_token)
    try:
        response = vk_.method('photos.get',
                              {
                                  'access_token': user_token,
                                  'v': V,
                                  'owner_id': user_owner_id,
                                  'album_id': 'profile',
                                  'count': 10,
                                  'extended': 1,
                                  'photo_sizes': 1,
                              })
    except ApiError:
        return 'нет доступа к фото'
    users_photos = []
    for i in range(10):
        try:
            users_photos.append(
                [response['items'][i]['count'],
                 'photo' + str(response['items'][i]['owner_id']) + '_' + str(response['items'][i]['id'])])
        except IndexError:
            users_photos.append(['нет фото.'])
    return users_photos


#json

def json_create(lst):
    today = datetime.date.today()
    today_str = f'{today.day}.{today.month}.{today.year}'
    res = {}
    res_list = []
    for num, info in enumerate(lst):
        res['data'] = today_str
        res['first_name'] = info[0]
        res['last_name'] = info[1]
        res['link'] = info[2]
        res['id'] = info[3]
        res_list.append(res.copy())

    with open("result.json", "a", encoding='UTF-8') as write_file:
        json.dump(res_list, write_file, ensure_ascii=False)

    print(f'Информация о загруженных файлах успешно записана в json файл.')
