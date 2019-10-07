# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Database(object):
    def setupUi(self, Database):
        Database.setObjectName("Database")
        Database.resize(637, 507)
        self.centralwidget = QtWidgets.QWidget(Database)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(510, 380, 84, 28))
        self.pushButton.setObjectName("pushButton")
        self.table = QtWidgets.QComboBox(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(70, 70, 131, 41))
        self.table.setObjectName("table")
        self.table.addItem("")
        self.table.addItem("")
        self.table.addItem("")
        self.table.addItem("")
        self.table.addItem("")
        self.action = QtWidgets.QComboBox(self.centralwidget)
        self.action.setGeometry(QtCore.QRect(270, 70, 151, 41))
        self.action.setObjectName("action")
        self.action.addItem("")
        self.action.addItem("")
        self.action.addItem("")
        self.action.addItem("")
        self.actLabel = QtWidgets.QLabel(self.centralwidget)
        self.actLabel.setGeometry(QtCore.QRect(50, 30, 291, 16))
        font = QtGui.QFont()
        font.setFamily("Ubuntu")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.actLabel.setFont(font)
        self.actLabel.setObjectName("actLabel")
        Database.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Database)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 637, 25))
        self.menubar.setObjectName("menubar")
        Database.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Database)
        self.statusbar.setObjectName("statusbar")
        Database.setStatusBar(self.statusbar)

        self.retranslateUi(Database)
        QtCore.QMetaObject.connectSlotsByName(Database)

    def retranslateUi(self, Database):
        _translate = QtCore.QCoreApplication.translate
        Database.setWindowTitle(_translate("Database", "MainWindow"))
        self.pushButton.setText(_translate("Database", "Action"))
        self.table.setItemText(0, _translate("Database", "cargo"))
        self.table.setItemText(1, _translate("Database", "department"))
        self.table.setItemText(2, _translate("Database", "worker"))
        self.table.setItemText(3, _translate("Database", "client"))
        self.table.setItemText(4, _translate("Database", "packing"))
        self.action.setItemText(0, _translate("Database", "add"))
        self.action.setItemText(1, _translate("Database", "delete"))
        self.action.setItemText(2, _translate("Database", "update"))
        self.action.setItemText(3, _translate("Database", "insert"))
        self.actLabel.setText(_translate("Database", "Choose table and action to do:"))

#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Database = QtWidgets.QMainWindow()
#     ui = Ui_Database()
#     ui.setupUi(Database)
#     Database.show()
#     sys.exit(app.exec_())
#
