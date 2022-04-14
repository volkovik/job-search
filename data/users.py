import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)

    specialization = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    count = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    # salary from
    # experience
    # work_time

    # favourites = orm.relationship('favourite', backref="jobs")
    # blacklist_jobs = orm.relation("Job",
    #                               secondary="blacklist",
    #                               backref="jobs"
    #                               )
