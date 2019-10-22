from view import *
from model import *
from cargo_d import *
import sys
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets

class CargoController( Ui_Dialog):
    def __init__(self, MainWindow,db):
        super().__init__(MainWindow)
        self.db = db
        self.columns = ' '
        self.pushButton.clicked.connect(self.getValues)

    def getValues(self):
        from_range = int(self.textEdit.toPlainText())
        to_range = int (self.textEdit_2.toPlainText())
        checked = str(not self.checkBox.checkState()==0).lower()

        req = " SELECT * FROM (SELECT * FROM cargo INNER JOIN worker ON cargo.worker_id = worker.id) AS result WHERE (estimated_value BETWEEN {0} AND {1}) AND \"Delivered\" = {2};".format(from_range, to_range,checked)
        #req = "select to_tsvector('note');"
        result = self.db.get_request(req)
        r_str = ""
        for i in result:
            for st in i:
                r_str += str(st) + "    "
            r_str += "\n"
        for word in self.db.colnames:
            self.columns += word + "\t"
        self.columns += '\n'
        self.plainTextEdit.setPlainText(self.columns + r_str)

class Controller(Ui_Database):
    def requestFormat(self, comboTable, comboAction, textAction):
        if comboAction == 'delete':
            self.ui.Flag = self.db.delete_request(comboTable, textAction)
            if not self.ui.Flag:
                self.error.setText('Error in sequence')
            else:
                self.error.setText('Done')
        elif comboAction == 'insert':
            self.ui.Flag = self.db.insert_request(comboTable, textAction)
            if not self.ui.Flag:
                self.error.setText('Error in sequence')
            else:
                self.error.setText('Done')
        elif comboAction == 'update':
            self.ui. Flag = self.db.update_request(comboTable, textAction)
            print(self.ui.Flag)
            if not self.ui.Flag:
                self.error.setText('Error in sequence')
            else:
                self.error.setText('Done')

    def gen_values(self):
        self.db.generate_values()

    def __init__(self, MainWindow):
        self.ui = Ui_Database(MainWindow)
        self.db = Database()
        super().__init__(MainWindow)

        self.pushButton.clicked.connect(self.saveInfo)
        self.genData.clicked.connect(self.gen_values)
        self.pushButton_2.clicked.connect(self.showDialog)
        self.search.clicked.connect(self.full_text_search)
        self.pushButton_3.clicked.connect(self.full_str)
        self.comboTable = None
        self.comboAction = None
        self.textAction = None
        self.columns = ' '
        self.full_text = ''
        self.full_search_table = ''
        self.Flag = True
        self.window = QtWidgets.QDialog(MainWindow)
        self.ui = CargoController(self.window, self.db)

    def saveInfo(self):
        self.comboAction = self.action.currentText()
        self.comboTable = self.table.currentText()
        self.textAction = self.textEdit.toPlainText()
        print(self.comboAction, self.comboTable, self.textAction)
        self.requestFormat(self.comboTable, self.comboAction, self.textAction)
        if not self.Flag:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Unable to perceive the rquest')
    def showDialog(self):
        self.window.show()

    def full_text_search(self):
        self.full_text = self.textSearch.toPlainText()
        self.full_search_table = self.full_text_box.currentText()
        self.full_text = self.full_text.split('=')
        try:
            req = "SELECT * FROM {1} WHERE {0} LIKE '%{2}%'".format(self.full_text[0], self.full_search_table, " ".join(self.full_text[1].split()))
            name = str(self.db.get_request(req))
            r_str = ''
            for i in name:
                for st in i:
                    r_str += str(st) + "    "
                r_str += "\n"
            for word in self.db.colnames:
                self.columns += word + "    "
            self.columns += '\n'
            self.textSearch.setText(self.columns + name)
        except:
            self.textSearch.setText("Error")


    def full_str(self):
        self.full_text = self.textSearch.toPlainText()
        self.full_search_table = self.full_text_box.currentText()
        self.full_text = self.full_text.split('=')
        req = "SELECT * FROM {1} WHERE {0} LIKE '{2}'".format(self.full_text[0], self.full_search_table, " ".join(self.full_text[1].split()))
        name = str(self.db.get_request(req))
        r_str = ''
        for i in name:
            for st in i:
                r_str += str(st) + "    "
            r_str += "\n"
        for word in self.db.colnames:
            self.columns += word + "    "
        self.columns += '\n'
        self.textSearch.setText(self.columns + name)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.show()
    cntr = Controller(MainWindow)

    sys.exit(app.exec_())
