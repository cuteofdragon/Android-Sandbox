from sqlalchemy.orm import sessionmaker, scoped_session

from lib.model import Application
from lib.model.Url import Url
from lib.model.database.Database import Database
from lib.modules.Module import Module

from pathlib import Path

import logging
import glob


class ModuleGeneral(Module):

    def __init__(self, application):
        Module.__init__(self,application)

    @staticmethod
    def select(path, **kwargs):
        logging.debug('ModuleGeneral:select()')
        if Path(path).is_file():
            return path
        else:
            return glob.glob(f"{path}/*.apk")

    def parse(self,message):
        logging.debug("ModuleGeneral:parse()")

        if(message.startswith('url:')):
            self.url(message[4:])
            return

    def url(self, url):
        logging.debug("ModuleGeneral:url()")

        # Create a thread local session
        engine = Database.get_engine()

        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        session = Session()
        Session.remove()

        # Fetch application for this session ( could not use self.application
        # because the usage must be thread local )
        application = session.query(Application.Application).get(self.application.id)
        url = Url(url)
        application.url.append(url)
        session.add(url)
        session.add(application)
        session.commit()

