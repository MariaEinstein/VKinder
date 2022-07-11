import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError
#token group(вставляем нужный)
#DB
Base = declarative_base()

engine = sq.create_engine('postgresql://_user:12345@localhost:5432/db_vkinder', client_encoding='utf8')

Session = sessionmaker(bind = engine)

#vk_api
vk_session = vk_api.VkApi(token = 'token group')
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


#DB
session = Session()
connection = engine.connect()



class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    vk_id = sq.Column(sq.Integer, unique=True)


class Photos(Base):
    __tablename__ = 'photos'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))



#functions DB

def check_db_master(ids):
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id


def write_msg(user_id, message, attachment=None):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment})


def register_user(vk_id):
    try:
        new_user = User(
            vk_id=vk_id
        )
        session.add(new_user)
        session.commit()
        return True
    except (IntegrityError, InvalidRequestError):
        return False



def add_user_photos(event_id, link_photo, id_user):
    try:
        new_user = Photos(
            link_photo=link_photo,
            id_user=id_user
        )
        session.add(new_user)
        session.commit()
        write_msg(event_id,
                  'Фото пользователя сохранено ')
        return True
    except (IntegrityError, InvalidRequestError):
        write_msg(event_id,
                  'Невозможно добавить фото этого пользователя(Уже сохранено)')
        return False


if __name__ == '__main__':
    Base.metadata.create_all(engine)


