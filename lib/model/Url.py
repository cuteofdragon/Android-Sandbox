import datetime
import re
import socket
from urllib.parse import urlparse

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime

from lib.model.database.Database import Database

Base = Database.get_declarative_base()


class Url(Base):
    __tablename__ = 'url'
    id = Column(Integer, primary_key=True)
    scheme = Column(String)
    domain = Column(String)
    uri = Column(String)
    ip = Column(String)
    query = Column(String)
    is_up = Column(Boolean)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    application_id = Column(Integer, ForeignKey('application.id'))

    def __init__(self, url):
        parsed_url = urlparse(url)
        self.scheme = parsed_url.scheme
        self.uri = parsed_url.path
        self.query = parsed_url.query

        if re.match(r'\d+\.\d+.\d+.\d+', parsed_url.netloc) :
            self.ip = parsed_url.netloc
            self.domain = None
            self.is_up = self.check_is_up(self.ip)

        else:
            self.domain = parsed_url.netloc
            try:
                self.ip = socket.gethostbyname(self.domain)
                self.is_up = True
            except:
                self.is_up = False


    def check_is_up(self,addr):
        try:
            socket.inet_aton(addr)
            return True
        except:
            return False



    def __repr__(self):
        return f'<Url(id={self.id}, scheme="{self.scheme}"' \
            f', domain="{self.domain}", uri="{self.uri}"' \
            f', is_up="{self.is_up}", date="{self.date}")>'