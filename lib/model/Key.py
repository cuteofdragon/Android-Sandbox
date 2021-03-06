import datetime

from lib.model.database.Database import Database

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey

Base = Database.get_declarative_base()


class Key(Base):
    __tablename__ = 'key'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    value = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    application_id = Column(Integer, ForeignKey('application.id'))

    def __init__(self, type, key):
        self.type = type
        self.key = key

    def __repr__(self):
        return f'<Key(id={self.id},type="{self.type}",value="{self.value}",date="{self.date}")>'
