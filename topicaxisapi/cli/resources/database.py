from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from topicaxisapi.configuration import Settings


class Database:
    def __init__(self):
        self.engine = None
        self.session = None

    def __enter__(self):
        settings = Settings()
        self.engine = create_engine(settings.sqlalchemy_url)
        Session = sessionmaker(self.engine)
        self.session = Session()

        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.session.close()
        self.engine.dispose()
