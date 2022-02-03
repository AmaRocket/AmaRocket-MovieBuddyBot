import datetime

from aiogram import types
from gino import Gino

from sqlalchemy import sql, desc
from gino.schema import GinoSchemaVisitor

from config import PG_PASS, PG_USER, PGHOST, DB_NAME

db = Gino()


class User(db.Model):
    __tablename__ = "users"
    query: sql.Select

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.BigInteger, unique=True)
    language = db.Column(db.String)
    first_name = db.Column(db.String)
    username = db.Column(db.String)
    time = db.Column(db.DateTime())

    def __repr__(self):
        return "<User(id='{}', users_id='{}', first_name='{}', username='{}', time='{}')>".format(
            self.id, self.users_id, self.first_name, self.username, self.time)


class Title(db.Model):
    __tablename__ = "title"
    query: sql.Select

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String)
    time = db.Column(db.DateTime())

    def __repr__(self):
        return "<Title(id='{}', users_id='{}', title='{}', time='{}')>".format(
            self.id, self.users_id, self.title, self.time)


class Criteria(db.Model):
    __tablename__ = "criteria"
    query: sql.Select

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    genre = db.Column(db.Integer)
    vote_average = db.Column(db.Integer)
    year = db.Column(db.Integer)
    time = db.Column(db.DateTime())

    def __repr__(self):
        return "<Title(id='{}', users_id='{}', genre='{}', vote_average='{}', year='{}', time='{}')>".format(
            self.id, self.users_id, self.genre, self.vote_average, self.year, self.time)


class MyMovies(db.Model):
    __tablename__ = "my_movies"
    query: sql.Select

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    movie_id = db.Column(db.Integer)
    time = db.Column(db.DateTime())
    data = db.Column(db.Text)

    __tableargs__ = (db.UniqueConstraint('users_id', 'movie_id'))

    def __repr__(self):
        return "<MyMovies(id='{}', users_id='{}', movie_id='{}', time='{}', data='{}')>".format(
            self.id, self.users_id, self.movie_id, self.time, self.data)


class DBCommands:
    async def get_user(self, user_id):
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_new_user(self):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.first_name = user.first_name
        new_user.time = datetime.datetime.now()

        await new_user.create()
        return new_user

    async def count_users(self):
        total = await db.func.count(User.id).gino.scalar()
        return total

    # For The FUTURE
    async def set_language(self, language):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        await user.update(language=language).apply()

    ###########################

    async def show_title(self):
        user_id = types.User.get_current().id
        title = await Title.query.where(Title.users_id == user_id).gino.all()
        return title

    async def show_criteria(self):
        user_id = types.User.get_current().id
        criteria = await Criteria.query.where(Criteria.users_id == user_id).gino.all()
        return criteria

    async def show_movies(self):
        user_id = types.User.get_current().id
        my_movies = await MyMovies.query.where(MyMovies.users_id == user_id).order_by(desc(MyMovies.id)).gino.all()
        return my_movies


    async def get_movie(self, movie_id):
        user_id = types.User.get_current().id
        drop = await MyMovies.query.where(MyMovies.movie_id == movie_id and MyMovies.users_id == user_id).gino.first()
        return drop

    ###########################


async def create_db():
    await db.set_bind(f'postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PGHOST}/{DB_NAME}')

    # Create tables
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()   # DROPPING DB
    await db.gino.create_all()
