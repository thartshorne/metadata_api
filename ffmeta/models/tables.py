from sqlalchemy import Table, Column, Numeric, Integer, String, ForeignKey, DateTime

from ffmeta.models.db import Base
response_table = Table('response', Base.metadata, autoload=True)