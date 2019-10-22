from view import *
from model import *
from cargo_d import *
import sys
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets

class CargoController( Ui_Dialog):
    def __init__(self, MainWindow,db):
        super().__init__(MainWindow)
        #self.setupUi(MainWindow)
        #self.temp = self.textEdit.toPlainText()
        self.pushButton.clicked.connect(self.getValues)
        self.db = db
        print('jfkjs')

    def getValues(self):
        print("dfgdfgdfg")
    #    from_range = int(self.textEdit.toPlainText())
    #    to_range = int (self.textEdit_2.toPlainText())
        checked =str(not self.checkBox.checkState()==0).lower()

        # req = "SELECT * FROM cargo WHERE (estimated_value BETWEEN {0} AND {1}) AND \"Delivered\" = {2};".format(from_range, to_range,checked)
       # req = " SELECT * FROM (SELECT * FROM cargo INNER JOIN worker ON cargo.worker_id = worker.id) AS result WHERE (estimated_value BETWEEN {0} AND {1});".format(from_range, to_range,checked)
        req = "select to_tsvector('notebook');"
        result = self.db.get_request(req)
        print(result)
        r_str =""
        for i in result:
            for st in i:
                r_str+=str(st) + " "
            r_str+="\n"
        print(r_str)
        self.plainTextEdit.setPlainText(r_str)


class Controller( Ui_Database):
    def requestFormat(self, comboTable, comboAction, textAction):
        self.temp = comboAction + comboTable
        print(comboAction)
        if comboAction == 'delete':
            self.ui.Flag = self.db.delete_request(comboTable, textAction)
        elif comboAction == 'insert':
            self.ui. Flag = self.db.insert_request(comboTable, textAction)
        elif comboAction == 'update':
            self.ui. Flag = self.db.update_request(comboTable, textAction)

    def gen_values(self):
        self.db.generate_values()

    def __init__(self, MainWindow):
        self.ui = Ui_Database(MainWindow)
        self.db = Database()
        super().__init__(MainWindow)

        self.pushButton.clicked.connect(self.saveInfo)
        self.genData.clicked.connect(self.gen_values)
        self.pushButton_2.clicked.connect(self.showDialog)

        self.comboTable = None
        self.comboAction = None
        self.textAction = None
        self.Flag = True
        self.window = QtWidgets.QDialog(MainWindow)
        self.ui = CargoController(self.window, self.db)

    def saveInfo(self):
        self.comboAction = self.action.currentText()
        self.comboTable = self.table.currentText()
        self.textAction = self.textEdit.toPlainText()
        print(self.comboAction, self.comboTable, self.textAction)
        print('func call')
        self.requestFormat(self.comboTable, self.comboAction, self.textAction)
        if not self.Flag:
            self.error_dialog = QtWidgets.QErrorMessage()
            self.error_dialog.showMessage('Unable to perceive the rquest')
    def showDialog(self):

        print(self.window)
        self.window.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.show()
    cntr = Controller(MainWindow)

    sys.exit(app.exec_())
