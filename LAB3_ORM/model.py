from sqlalchemy import Table, Column, create_engine, insert, delete, text, select, update
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, ForeignKey, String, Unicode, Numeric, Boolean, DateTime, TIMESTAMP, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relation
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import json
import random
import string
import datetime

DeclarativeBase = declarative_base()
# metadata = DeclarativeBase.metadata
#
#
# class RefCargoWorker(DeclarativeBase):
#     __tablename__ = 'ref_worker_cargo'
#
#     cargo_barcode = Column('cargo_barcode', String, ForeignKey('cargo.barcode'))
#     worker_id = Column('worker_id', Integer, ForeignKey('worker.id'))
#     time = Column('time', TIMESTAMP, primary_key=True)
#
#
# class RefClientWorker(DeclarativeBase):
#     __tablename__ = 'ref_client_worker'
#
#     worker_id = Column('worker_id', Integer, ForeignKey('worker.id'))
#     client_number = Column('client_number', String, ForeignKey('client.client_number'))
#     time = Column('time', TIMESTAMP, primary_key=True)
#
#
# class Client(DeclarativeBase):
#     __tablename__ = "client"
#
#     full_name = Column("full_name", String)
#     client_number = Column("client_number", String, primary_key=True)
#     client_type = Column("client_type", String)
#     client_id_ref = relationship("Cargo")
#     ref_client_worker = relationship("Worker", secondary='ref_client_worker')
#
#     def __repr__(self):
#         return f'Client : {self.full_name, self.client_number, self.client_type}'
#
# class Worker(DeclarativeBase):
#     __tablename__ = "worker"
#
#     id = Column(Integer, primary_key=True)
#     full_name = Column("full_name", String)
#     position = Column("position", String)
#     working_hours = Column("working_hours", String)
#     salary = Column(Integer)
#     dep_number = Column(Integer, ForeignKey("department.number_d", ondelete="CASCADE"))
#     ref_worker_cargo = relationship("Cargo", secondary='ref_worker_cargo')
#     ref_worker_client = relationship(Client, secondary='ref_client_worker')
#
#
# class Department(DeclarativeBase):
#     __tablename__ = "department"
#
#     number_d = Column(Integer, primary_key=True)
#     address = Column("address", String)
#     d_type = Column("d_type", String)
#     street_number = Column("street_number", String(10))
#     ch_worker_numb = relationship("Worker")
#
#
# class Cargo(DeclarativeBase):
#     __tablename__ = "cargo"
#
#     barcode = Column(String, primary_key=True)
#     cargo_type = Column(String)
#     estimated_value = Column(Numeric)
#     client_id = Column(String, ForeignKey("client.client_number", ondelete="CASCADE"))
#     worker_id = Column(String, ForeignKey("worker.id", ondelete="CASCADE"))
#     delivered = Column(Boolean, unique=False, default=True)
#     ref_cargo_packing = relationship("Packing")
#
#     ref_cargo_worker = relationship("Cargo", secondary='ref_worker_cargo')
#
#
# class Packing(DeclarativeBase):
#     __tablename__ = 'packing'
#
#     packing_code = Column(Integer, primary_key=True)
#     packing_type = Column(String)
#     amount = Column(Integer)
#     price = Column(Numeric)
#     weight = Column(Numeric)
#     cargo_barcode = Column(String, ForeignKey("cargo.barcode", ondelete="CASCADE"))

#
# DeclarativeBase.metadata.create_all()


def randomString(stringLength=8, flag=True):
    """Generate a random string with the combination of lowercase and uppercase letters """
    if flag:
        letters = string.ascii_letters + ' '
    else:
        letters = string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


class Database:

    def __init__(self):
        try:
            self.engine = create_engine('postgresql://postgres:6969@localhost:5433/postgres')
            session_class = sessionmaker(bind=self.engine)
            self.metadata = MetaData() #DeclarativeBase.metadata
            self.metadata.reflect(self.engine)
            self.base = automap_base(metadata=self.metadata)
            self.base.prepare()
            session_class = sessionmaker(bind=self.engine)

            self.session = session_class()
            st = self.base.classes['client']
            print(st)

        except ArgumentError:
            print('Argument error')

    def delete_all(self):
        """
        It deletes all items and all lists
        """
        self.session.query(self.base.classes['client']).delete()
        self.session.query(self.base.classes['cargo']).delete()
        self.session.query(self.base.classes['department']).delete()
        self.session.query(self.base.classes['packing']).delete()
        self.session.query(self.base.classes['worker']).delete()
        self.session.query(self.base.classes['ref_worker_cargo']).delete()
        self.session.query(self.base.classes['ref_client_worker']).delete()
        self.session.commit()

    def save_all(self, objects):
        """
        It commits objects created by outer scope
        :param objects: a list of objects to save
        """
        self.session.add_all(objects)
        self.session.commit()

    def delete_request(self, table, where):
        '''
        deletes the row with condition where
        :param table: name of the table
        :param where: condition to delete
        :return:
        '''
        temp = Table(table, self.metadata, autoload=True, autoload_with=self.engine)
        query = delete(temp).where(text(str(where)))
        results = self.session.execute(query)
        results = self.session.execute(select([temp])).fetchall()
        self.session.commit()

    def insert_request(self, table, condition):
        temp = Table(table, self.metadata, autoload=True, autoload_with=self.engine)
        res = eval('dict(' + condition + ')')
        query = insert(temp)
        ResultProxy = self.session.execute(query, res)
        self.session.commit()

    def update_request(self, table, condition):
        temp = Table(table, self.metadata, autoload=True, autoload_with=self.engine)
        where, what = condition.split(',')
        res = eval('dict(' + what + ')')
        query = update(temp).values(res).where(text(where))
        results = self.session.execute(query)
        # results = self.session.execute(select([temp])).fetchall()
        self.session.commit()

    def requestFormat(self, comboTable, comboAction, textAction, Controller):
        Controller.gen_label.setText('')

        if comboAction == 'delete':
            try:
                self.delete_request(comboTable, textAction)
                Controller.error.setText('Done')

            except Exception as error:
                Controller.error.setText(str(error))
        elif comboAction == 'insert':
            try:
                self.insert_request(comboTable, textAction)
                Controller.error.setText('Done')

            except Exception as error:
                Controller.error.setText(str(error))
        elif comboAction == 'update':
            try:
                self.update_request(comboTable, textAction)
                Controller.error.setText('Done')

            except Exception as error:
                 Controller.error.setText(str(error))


    def generate_values(self):
        with open('data.json', 'r+') as f:
            data = json.load(f)
        start_last_number = data['last_number'] + 1
        start_estimated_value = data['estimated_value'] + 1
        time = data['date']
        amount = 20
        dep = Table('department', self.metadata, autoload=True, autoload_with=self.engine)
        worker = Table('worker', self.metadata, autoload=True, autoload_with=self.engine)
        client = Table('client', self.metadata, autoload=True, autoload_with=self.engine)
        cargo = Table('cargo', self.metadata, autoload=True, autoload_with=self.engine)
        packing = Table('packing', self.metadata, autoload=True, autoload_with=self.engine)
        cargo_worker = Table('ref_worker_cargo', self.metadata, autoload=True, autoload_with=self.engine)
        client_worker = Table('ref_client_worker', self.metadata, autoload=True, autoload_with=self.engine)

        values_dep =list()
        values_worker = list()
        values_client = list()
        values_cargo = list()
        values_packing = list()
        values_ref_client_worker = list()
        values_ref_worker_cargo = list()
        curr  = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

        for i in range(start_last_number, start_last_number+amount):
        #     print(i)
            temp = randomString(10, False)

            if i%2 == 0:
                    values_dep.append({'number_d': i, 'address': randomString(10, True), 'd_type': 'postal', 'street_number': random.randint(1, 500)})
                    values_worker.append({'id': i, 'full_name': randomString(10, True), 'position': 'casher', 'working_hours': randomString(5, False), 'salary': random.randint(7000, 15000), 'dep_number': i})
                    values_cargo.append({'barcode': i, 'cargo_type': randomString(20, True), 'estimated_value': random.randint(200, 1000), 'client_id': temp, 'worker_id': i, 'delivered': False})
                    values_client.append({'full_name': randomString(20, True), 'client_type' : 'recipient', 'client_number': temp}) #TODO randomString with numbers
            else:
                values_dep.append({'number_d': i, 'address': randomString(10, True), 'd_type': 'cargo','street_number': random.randint(1, 500)})
                values_worker.append({'id': i, 'full_name': randomString(10, True), 'position': 'heavier','working_hours': randomString(5, False), 'salary': random.randint(7000, 15000),'dep_number': i})
                values_cargo.append({'barcode': i, 'cargo_type': randomString(20, True), 'estimated_value': random.randint(200, 1000), 'client_id': temp, 'worker_id': i, 'delivered': True})
                values_client.append({'full_name': randomString(20, True), 'client_type' : 'sender', 'client_number': temp}) #TODO randomString with numbers
            values_packing.append({'packing_code': i, 'packing_type': randomString(10, True), 'amount': random.randint(1, 10), 'price': random.randint(1, 36), 'weight': random.randint(1, 30), 'cargo_barcode': i})
            values_ref_client_worker.append({'worker_id': i, 'client_number': temp, 'time': curr})
            values_ref_worker_cargo.append({'worker_id': i, 'cargo_barcode': i, 'time': curr})

            curr += datetime.timedelta(minutes=random.randrange(1, 20000))

        data = {'last_number': start_last_number + amount, 'estimated_value': start_estimated_value + amount, 'date': str(curr)}
        with open('data.json', 'w+') as f:
            json.dump(data, f)

        self.session.execute(insert(dep, values_dep))
        self.session.execute(insert(worker, values_worker))
        self.session.execute(insert(client, values_client))
        self.session.execute(insert(cargo, values_cargo))
        self.session.execute(insert(packing, values_packing))
        self.session.execute(insert(cargo_worker, values_ref_worker_cargo))
        self.session.execute(insert(client_worker, values_ref_client_worker))

        self.session.commit()

    def gen_values(self, Controller):
        print(Controller)
        self.generate_values()
        # if self.Gen:
        # Controller.gen_label.setText('Done!')
        # else:
        # Controller.gen_label.setText('Error while generating!')

