import datetime

from lib.model.database.Database import Database

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey

Base = Database.get_declarative_base()


class SharedPreferences(Base):
    __tablename__ = 'shared_preferences'

    id = Column(Integer, primary_key=True)
    value = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    application_id = Column(Integer, ForeignKey('application.id'))

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<SharedPreferences(id={self.id},value="{self.value}",date="{self.date}")>'
