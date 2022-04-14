import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase

HHRU_CODE = 0
SUPERJOB_CODE = 1


class FavouriteTable(SqlAlchemyBase):
    __tablename__ = 'favourite'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    job_id = sqlalchemy.Column(sqlalchemy.Integer)


class Job(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    job_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    source = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
