
from androguard.misc import APK

import hashlib
import logging

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


from lib.model.database.Database import Database
from lib.model.Url import Url

logging.getLogger("androguard").setLevel(logging.CRITICAL)
logging.getLogger("dad").setLevel(logging.CRITICAL)

Base = Database.get_declarative_base()


class Application(Base ,APK, ):

    __tablename__ = 'application'
    id = Column(Integer, primary_key=True)
    package = Column(String)
    path = Column(String)
    sha256 = Column(String)
    analysis_id = Column(Integer, ForeignKey('analysis.id'))
    url = relationship("Url")
    key = relationship("Key")


    def __init__(self, path):
        APK.__init__(self, path)
        self.path = str(path)
        self.get_sha256_hash()

    def get_sha256_hash(self):
        if self.sha256 is None:
            sha256_hash = hashlib.sha256()
            with open(self.path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            self.sha256 = sha256_hash.hexdigest()
        return self.sha256
