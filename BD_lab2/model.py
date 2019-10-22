import psycopg2 as ps
from configparser import ConfigParser
import datetime
from datetime import timedelta

import json


class Database:
    def config(self, filename='config.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        return db

    def get_request(self, req):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            self.colnames = [desc[0] for desc in cursor.description]
            print(self.colnames)
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False


    def __init__(self):
        self.conn = None
        self.colnames = list()
        try:
            params = self.config('config.ini')
            self.conn = ps.connect(**params)

        except(Exception, ps.DatabaseError) as error:
            print(error)

    def delete_request(self, action, text):
        return self.request("DELETE FROM {0} WHERE {1};".format(action, text))

    def insert_request(self, table, text):
        print(text)
        enter = [list.split('=') for list in text.split(',')] #devided values
        values = arguments = str()
        for word in enter:
            arguments += word[0] + ','
            values += word[1] + ','
        arguments = arguments[:-1]
        values = values[:-1]
        print(values)
        return self.request("INSERT INTO {0} ({1}) VALUES ({2}) ".format(table, arguments, values))


    def request(self, req):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            print('sdd')
            self.conn.commit()
            print("fgnkjfg")
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False


    def update_request(self, table, text):
        property = text.split('\n')
        print(property)
        print("UPDATE {0} SET {1} WHERE {2}".format(table, property[1], property[0]))
        return self.request("UPDATE {0} SET {1} WHERE {2}".format(table, property[1], property[0]))

    #    dab = cursor.fetchall()
    #    print(dab)
    #     cursor.close()
    def generate_values(self):
        with open('data.json', 'r+') as f:
            data = json.load(f)
        print(data)
        start_last_number = data['last_number']+1
        start_estimated_value = data['estimated_value']+1
        self.request("INSERT INTO department (address, number_d, d_type, street_number) VALUES (get_random_string (9),generate_series({0}, {1}), 'cargo', generate_series({0}, {1}));".format(start_estimated_value, start_estimated_value+10))
        self.request("INSERT INTO worker (id, full_name, position, working_hours, salary, dep_number) VALUES (generate_series({0},{1}), md5(random()::text), 'manager' , md5(random()::text), generate_series(10000, 10000+10), generate_series({0}, {1}));".format(start_estimated_value, start_estimated_value+10 ))
        self.request("INSERT INTO client (full_name, client_type, client_number) VALUES (get_random_string (9), 'sender',generate_series({0}, {1}));".format(start_last_number, start_last_number+10))
        self.request("INSERT INTO cargo (barcode, cargo_type, estimated_value, client_id, worker_id, \"Delivered\" ) VALUES (generate_series({2}, {3}), md5(random()::text), generate_series({0},{1}), generate_series({2},{3}), generate_series({0},{1}), true);".format(start_estimated_value, start_estimated_value+10, start_last_number, start_last_number+10))
        self.request("INSERT INTO packing (packing_code, packing_type, amount, price, weight, cargo_barcode, is_embedded) VALUES (generate_series({0}, {1}), get_random_string (9), generate_series({2}, {3}), generate_series({3}, {2}, -1), generate_series({2}, {3}), generate_series({0}, {1}), false);".format(start_last_number, start_last_number+10, 10, 20))
        self.request("INSERT INTO ref_worker_cargo (cargo_barcode, worker_id, time) VALUES (generate_series({0}, {1}), generate_series({2}, {3}), generate_series('{4}'::timestamp, '{5}','24 hours'));".format(start_last_number, start_last_number+10, start_estimated_value, start_estimated_value+10, str(datetime.datetime.now()), str( datetime.datetime.now() + timedelta(days=10))))
        
        self.request("INSERT INTO ref_client_worker ( worker_id, client_number, time) VALUES (generate_series({2}, {3}), generate_series({0}, {1}), generate_series('{4}'::timestamp, '{5}','24 hours'));".format(start_last_number, start_last_number+10, start_estimated_value, start_estimated_value+10,  str(datetime.datetime.now()), str( datetime.datetime.now() + timedelta(days=10))))
        data = {'last_number': start_last_number + 10, 'estimated_value': start_estimated_value + 10}
        with open('data.json', 'w+') as f:
            json.dump(data, f)




