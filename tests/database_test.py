from sqlalchemy import Column, Integer, String, Date, create_engine, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from lib.model.Application import Application
from lib.model.Url import Url
from lib.model.database.Database import Database
from lib.model.Analysis import Analysis

import uuid
import datetime

import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("../config/config.ini")

    Database.set_configuration(config)
    print(Analysis,Application,Url)

    engine = Database.get_engine()
    Database.get_declarative_base().metadata.create_all(engine)

    url = Url()
    application = Application("test.apk")
    application.url.append(url)
    analysis = Analysis(uuid=str(uuid.uuid4()), date=datetime.datetime.now())
    analysis.application.append(application)

    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(analysis)
    session.add(application)
    session.add(url)
    session.commit()
