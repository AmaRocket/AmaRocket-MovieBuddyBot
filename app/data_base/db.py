from aiogram import types, Bot
from gino import Gino
from sqlalchemy import (Column, Integer, BigInteger, String,
                        Sequence, TIMESTAMP, Boolean, JSON)
from sqlalchemy import sql
from gino.schema import GinoSchemaVisitor

from config import PG_PASS, PG_USER, PGHOST, DB_NAME

db = Gino()


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String(2))
    full_name = Column(String(100))
    username = Column(String(50))
    query: sql.Select

    # def __repr__(self):
    #     return "<User(id='{}', fullname='{}', username='{}')>".format(
    #         self.id, self.full_name, self.username)
    #


class Title(db.Model):
    __tablename__ = "title"
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    title = Column(String(250))
    time = Column(TIMESTAMP)


class Criteria(db.Model):
    __tablename__ = "criteria"
    query: sql.Select

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    genre = Column(String(250))
    vote_average = Column(String(250))
    year = Column(String(250))
    time = Column(TIMESTAMP)


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
        new_user.full_name = user.full_name

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


async def create_db():
    await db.set_bind(f'postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PGHOST}/{DB_NAME}')

    # Create tables
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()
    await db.gino.create_all()