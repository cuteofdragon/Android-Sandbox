from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    _engine = None
    _configuration = None
    _base = None
    _session = None

    @staticmethod
    def set_configuration(configuration):
        Database._configuration = configuration

    @staticmethod
    def get_engine():
        if Database._engine is None:
            Database._engine = create_engine(Database._configuration['DATABASE'].get('url'), echo=True, connect_args={'check_same_thread': False})
        return Database._engine

    @staticmethod
    def get_declarative_base():
        if Database._base is None:
            Database._base = declarative_base()
        return Database._base

    @staticmethod
    def get_session():
        if Database._session is None :
            Database.get_declarative_base().metadata.create_all(Database.get_engine())
            Session = sessionmaker(bind=Database.get_engine())
            Database._session = Session()
        return Database._session
