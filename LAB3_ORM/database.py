from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import *


class Database:
    pass
    def __init__(self):
        engine = create_engine('postgresql://postgres:6969@localhost:5433/postgres')
        session_class = sessionmaker(bind=engine)
        self.session = session_class()

    def delete_all(self):
        """
        It deletes all items and all lists
        """
        self.session.query(Worker).delete()
        self.session.query(Client).delete()
        self.session.query(Cargo).delete()
        self.session.query(Department).delete()
        self.session.query(Packing).delete()
        self.session.query(RefCargoWorker).delete()
        self.session.query(RefClientWorker).delete()

    def save_all(self, objects):
        """
        It commits objects created by outer scope
        :param objects: a list of objects to save
        """
        self.session.add_all(objects)
        self.session.commit()
