import os
from datetime import datetime
from typing import Dict

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String, asc, cast, desc, inspect, or_
from sqlalchemy.ext import declarative
from sqlalchemy.orm.attributes import InstrumentedAttribute
from werkzeug.exceptions import BadRequest

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

db = SQLAlchemy(session_options={"autoflush": False})


def declarative_base(cls):
    return declarative.declarative_base(cls=cls)


@declarative_base
class Base(object):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        index=True,
        nullable=True,
    )

    @classmethod
    def query_by_id(cls, id: int):
        row = db.session.query(cls).filter_by(id=id).first()
        return row

    @classmethod
    def filtration(cls, args: Dict):

        def inspect_field(field: String) -> InstrumentedAttribute:
            if field not in inspect(cls).all_orm_descriptors:
                raise BadRequest({"message": "Invalid field search requested"})
            field = getattr(cls, field)
            return field

        query = db.session.query(cls)
        for field, value in args.items():

            if ":neq" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(or_(filter_by != val for val in value.split(",")))
            elif ":eq" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(or_(filter_by == val for val in value.split(",")))
            elif ":gte" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(filter_by >= value)
            elif ":lte" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(filter_by <= value)
            elif ":lt" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(filter_by < value)
            elif ":gt" in field:
                filter_by = inspect_field(field.split(":")[0])
                query = query.filter(filter_by > value)
            elif ":like" in field:
                filter_by = inspect_field(field.split(":")[0])
                filter_by = cast(filter_by, String)
                query = query.filter(filter_by.ilike("%" + value + "%"))
        if "order_by" in args:
            for ordering in reversed(args["order_by"].split(",")):
                field, order = ordering.split(":")
                if order == "desc":
                    query = query.order_by(desc(inspect_field(field)))
                else:
                    query = query.order_by(asc(inspect_field(field)))
        else:
            query = query.order_by(desc(inspect_field("updated_at")))
        total_rows = query.count()
        if "start" in args and "limit" in args and int(args["start"]) > 0:
            query = query.offset((int(args["start"]) - 1) * int(args["limit"]))
            query = query.limit(int(args["limit"]))
        all_rows = query.all()
        return all_rows, total_rows
