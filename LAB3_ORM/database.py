from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import *
import json
import random
import string
import datetime


# TODO: error debugger in application


def randomString(stringLength=8, flag=True):
    """Generate a random string with the combination of lowercase and uppercase letters """
    if flag:
        letters = string.ascii_letters + ' '
    else:
        letters = string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))


class Database:

    def __init__(self):
        self.engine = create_engine('postgresql://postgres:6969@localhost:5433/postgres')
        session_class = sessionmaker(bind=self.engine)
        self.session = session_class()
        self.metadata = DeclarativeBase.metadata

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
            self.delete_request(comboTable, textAction)
            # if not Controller.Flag:
            #     Controller.error.setText(str(self.error))
            # else:
            #     Controller.error.setText('Done')
        elif comboAction == 'insert':
            self.insert_request(comboTable, textAction)
            # if not self.Flag:
            #     Controller.error.setText(str(self.error))
            # else:
            #     Controller.error.setText('Done')
        elif comboAction == 'update':
            self.update_request(comboTable, textAction)
        #     if not self.Flag:
        #         Controller.error.setText(str(self.error))
        #     else:
        #         Controller.error.setText('Done')

    def generate_values(self):
        with open('data.json', 'r+') as f:
            data = json.load(f)
        start_last_number = data['last_number'] + 1
        start_estimated_value = data['estimated_value'] + 1
        time = data['date']
        amount = 100
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
            values_dep.append({'number_d': i, 'address': randomString(10, True), 'd_type': 'postal', 'street_number': random.randint(1, 500)})
            values_worker.append({'id': i, 'full_name': randomString(10, True), 'position': 'casher', 'working_hours': randomString(5, False), 'salary': random.randint(7000, 15000), 'dep_number': i})
            temp = randomString(10, False)
            values_client.append({'full_name': randomString(20, True), 'client_type' : 'recipient', 'client_number': temp}) #TODO randomString with numbers
            values_cargo.append({'barcode': i, 'cargo_type': randomString(20, True), 'estimated_value': random.randint(200, 1000), 'client_id': temp, 'worker_id': i, 'delivered': False})
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

