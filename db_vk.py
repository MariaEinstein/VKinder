import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import token_group
from random import randrange
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError

# DB
Base = declarative_base()

engine = sq.create_engine('postgresql://_user:12345@localhost/db_vkinder', client_encoding='utf8')

Session = sessionmaker(bind=engine)

# vk_api
vk = vk_api.VkApi(token=token_group)
longpoll = VkLongPoll(vk)

# DB
session = Session()
connection = engine.connect()


class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)



class DatingUser(Base):
    __tablename__ = 'dating_user'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    id_user = sq.Column(sq.Integer, sq.ForeignKey('user.id', ondelete='CASCADE'))



class Photos(Base):
    __tablename__ = 'photos'
    id = sq.Column(sq.Integer, primary_key=True, autoincrement=True)
    link_photo = sq.Column(sq.String)
    count_likes = sq.Column(sq.Integer)
    id_dating_user = sq.Column(sq.Integer, sq.ForeignKey('dating_user.id', ondelete='CASCADE'))


# functions DB

def check_db_master(ids):
    current_user_id = session.query(User).filter_by(vk_id=ids).first()
    return current_user_id


def msg_send(user_id, message, attachment=None):
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'random_id': randrange(10 ** 7),
               'attachment': attachment})



def check_db_user(ids):
    dating_user = session.query(DatingUser).filter_by(
        vk_id=ids).first()
    return dating_user

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
        msg_send(event_id,
                 'Фото пользователя сохранено ')
        return True
    except (IntegrityError, InvalidRequestError):
        msg_send(event_id,
                 'Невозможно добавить фото этого пользователя(Уже сохранено)')
        return False


if __name__ == '__main__':
    Base.metadata.create_all(engine)
