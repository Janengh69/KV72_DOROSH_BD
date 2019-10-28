import psycopg2 as ps
from configparser import ConfigParser
import datetime
from datetime import timedelta
import pandas as pd
import plotly
from terminaltables import AsciiTable
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
            cursor.execute(req)
            self.conn.commit()
            self.colnames = [desc[0] for desc in cursor.description]
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            self.conn.rollback()
            self.gen_error = error
            self.erFlag= True
            print(error)
            return False


    def __init__(self):
        self.conn = None
        self.error = ''
        self.gen_error = ''
        self.erFlag = True
        self.Gen = True
        self.colnames = list()
        try:
            params = self.config('config.ini')
            self.conn = ps.connect(**params)

        except(Exception, ps.DatabaseError) as error:
            print(error)

    def delete_request(self, action, text):
        return self.request("DELETE FROM {0} WHERE {1};".format(action, text))

    def insert_request(self, table, text):
        enter = [list.split('=') for list in text.split(',')] #devided values
        values = arguments = str()
        for word in enter:
            arguments += word[0] + ','
            values += word[1] + ','
        arguments = arguments[:-1]
        values = values[:-1]
        return self.request("INSERT INTO {0} ({1}) VALUES ({2}) ".format(table, arguments, values))


    def request(self, req):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.error = error
            self.conn.rollback()
            return False

    def getValues(self, Cargo):
        from_range = int(Cargo.textEdit.toPlainText())
        to_range = int (Cargo.textEdit_2.toPlainText())
        checked = str(not Cargo.checkBox.checkState()==0).lower()


        req = " SELECT * FROM (SELECT * FROM cargo INNER JOIN worker ON cargo.worker_id = worker.id) AS result WHERE (estimated_value BETWEEN {0} AND {1}) AND delivered = {2};".format(from_range, to_range,checked)
        result = self.get_request(req)
        r_str = ""
        for i in result:
            for st in i:
                r_str += str(st) + "    "
            r_str += "\n"
        for word in self.colnames:
            Cargo.columns += word + "\t"
        Cargo.columns += '\n'
        Cargo.plainTextEdit.setPlainText(Cargo.columns + r_str)

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
        self.Gen = False
        start_last_number = data['last_number']+1
        start_estimated_value = data['estimated_value']+1
        amount = 20
        self.Gen= self.request("INSERT INTO department (address, number_d, d_type, street_number) VALUES (get_random_string (9),generate_series({0}, {1}), 'cargo', generate_series({0}, {1}));".format(start_estimated_value, start_estimated_value+amount))

        self.Gen= self.request("INSERT INTO worker (id, full_name, position, working_hours, salary, dep_number) VALUES (generate_series({0},{1}), md5(random()::text), 'heavier' , md5(random()::text), generate_series(10000, 10000+{2}), generate_series({0}, {1}));".format(start_estimated_value, int(start_estimated_value+amount/2), int(amount/2)))
        self.Gen= self.request("INSERT INTO worker (id, full_name, position, working_hours, salary, dep_number) VALUES (generate_series({0},{1}), md5(random()::text), 'casher' , md5(random()::text), generate_series(10000+{2}, 10000+{3}), generate_series({0}, {1}));".format(int(start_estimated_value+amount/2+1), start_estimated_value+amount, int(amount/2+1), amount))

        self.Gen= self.request("INSERT INTO client (full_name, client_type, client_number) VALUES (get_random_string (9), 'sender',generate_series({0}, {1}));".format(start_last_number, int(start_last_number+amount/2)))
        self.Gen= self.request("INSERT INTO client (full_name, client_type, client_number) VALUES (get_random_string (9), 'recipient',generate_series({0}, {1}));".format(int(start_last_number+ amount/2+1), start_last_number+amount))
        print(start_estimated_value)

        self.Gen= self.request("INSERT INTO cargo (barcode, cargo_type, estimated_value, client_id, worker_id, delivered ) VALUES (generate_series({2}, {3}), md5(random()::text), generate_series({0},{1}), generate_series({2},{3}), generate_series({0},{1}), true);".format(start_estimated_value, int(start_estimated_value+(amount/2)), start_last_number, int(start_last_number+amount/2)))
        self.Gen= self.request("INSERT INTO cargo (barcode, cargo_type, estimated_value, client_id, worker_id, delivered ) VALUES (generate_series({2}, {3}), md5(random()::text), generate_series({0},{1}), generate_series({2},{3}), generate_series({0},{1}), false);".format(int(start_estimated_value+ amount/2+1), start_estimated_value+amount, int(start_last_number+amount/2+1), start_last_number+amount))


        self.Gen= self.request("INSERT INTO packing (packing_code, packing_type, amount, price, weight, cargo_barcode) VALUES (generate_series({0}, {1}), get_random_string (9), generate_series({2}, {3}), generate_series({3}, {2}, -1), generate_series({2}, {3}), generate_series({0}, {1}));".format(start_last_number, start_last_number+amount, amount, 2*amount))
        self.Gen= self.request("INSERT INTO ref_worker_cargo (cargo_barcode, worker_id, time) VALUES (generate_series({0}, {1}), generate_series({2}, {3}), generate_series('{4}'::timestamp, '{5}','24 hours'));".format(start_last_number, start_last_number+amount, start_estimated_value, start_estimated_value+amount, str(datetime.datetime.now()), str( datetime.datetime.now() + timedelta(days=amount))))

        self.request("INSERT INTO ref_client_worker ( worker_id, client_number, time) VALUES (generate_series({2}, {3}), generate_series({0}, {1}), generate_series('{4}'::timestamp, '{5}','24 hours'));".format(start_last_number, start_last_number+amount, start_estimated_value, start_estimated_value+amount,  str(datetime.datetime.now()), str( datetime.datetime.now() + timedelta(days=amount))))
        data = {'last_number': start_last_number + amount, 'estimated_value': start_estimated_value + amount}
        with open('data.json', 'w+') as f:
            json.dump(data, f)


    def gen_values(self, Controller):
        print(Controller)
        self.generate_values()
        if self.Gen:
            Controller.gen_label.setText('Done!')
        else:
            Controller.gen_label.setText('Error while generating!')

    def requestFormat(self, comboTable, comboAction, textAction, Controller):
        Controller.gen_label.setText('')

        if comboAction == 'delete':
            Controller.Flag = self.delete_request(comboTable, textAction)
            if not Controller.Flag:
                Controller.error.setText(str(self.error))
            else:
                Controller.error.setText('Done')
        elif comboAction == 'insert':
            self.Flag = self.insert_request(comboTable, textAction)
            if not self.Flag:
                Controller.error.setText(str(self.error))
            else:
                Controller.error.setText('Done')
        elif comboAction == 'update':
            self.Flag = self.update_request(comboTable, textAction)
            if not self.Flag:
                Controller.error.setText(str(self.error))
            else:
                Controller.error.setText('Done')

    def full_string(self, Controller):
        self.columns = str()
        Controller.full_text = Controller.textSearch.toPlainText().split('=')
        Controller.full_search_table = Controller.full_text_box.currentText()       # from which table to search
        print(Controller.full_text)
        print(Controller.full_search_table)
        if len(Controller.full_text) == 1:
            Controller.textSearch.setText('Wrong entering')
            return
        req = ''
        temp = ''
        req = "SELECT * FROM {1} WHERE  to_tsvector({0}) @@ phraseto_tsquery('{2}');".format(Controller.full_text[0], Controller.full_search_table, " ".join(Controller.full_text[1].split()))
        name = self.get_request(req)
        if len(Controller.full_text) == 1:
            Controller.textSearch.setText('Wrong entering')
            return
        if self.erFlag:
            Controller.textSearch.setText(str(self.gen_error))
            return
        for word in name:
            for i in word:
                temp += str(i) + ' '
            temp+= '\n'
        for word in self.colnames:
            Controller.columns += word + "          "
        Controller.columns += '\n'
        Controller.textSearch.setText(self.columns + temp)

    def word_only(self, Controller):
        Controller.full_text = Controller.textSearch.toPlainText()
        Controller.full_search_table = Controller.full_text_box.currentText()
        Controller.full_text = Controller.full_text.split('=')
        template = ''
        if len(Controller.full_text) == 1:
            Controller.textSearch.setText('Wrong entering')
            return
        if self.erFlag:
            Controller.textSearch.setText(str(self.gen_error))
            return
        for word in Controller.full_text[1].strip().split(' '):
            template += "'" + word + "'" + '::tsquery || '
        temp=' '
        temp = str(map(lambda word: "'" + word + "'" + '::tsquery || ',Controller.full_text[1].strip().split(' ')))
        template = template[:-3]
        req = "SELECT * FROM {1} WHERE to_tsvector({0}) @@ ({2})".format(Controller.full_text[0].strip(), Controller.full_search_table, template)

        name = self.get_request(req)
        Controller.columns = str()
       # table = AsciiTable(name)
       # print(table.table)
        temp = str()
        for word in name:
            for i in word:
                temp += str(i) + '  '
            temp+= '\n'
        for word in self.colnames:
            self.colnames += word + "          "
        self.colnames += '\n'
        Controller.textSearch.setText(self.colnames + temp)