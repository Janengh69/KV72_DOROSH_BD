# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Database(object):
    def __init__(self, Database):
        Database.setObjectName("Database")
        Database.resize(639, 507)
        self.centralwidget = QtWidgets.QWidget(Database)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(510, 150, 84, 28))
        self.pushButton.setObjectName("pushButton")
        self.table = QtWidgets.QComboBox(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(30, 70, 131, 41))
        self.table.setObjectName("table")
        self.table.addItem("")
        self.table.addItem("")
        self.table.addItem("")
        self.table.addItem("")
        self.table.addItem("")
        self.action = QtWidgets.QComboBox(self.centralwidget)
        self.action.setGeometry(QtCore.QRect(200, 70, 151, 41))
        self.action.setObjectName("action")
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
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(390, 50, 181, 70))
        self.textEdit.setObjectName("textEdit")
        self.genData = QtWidgets.QPushButton(self.centralwidget)
        self.genData.setGeometry(QtCore.QRect(30, 140, 451, 61))
        self.genData.setObjectName("genData")
        self.textSearch = QtWidgets.QTextEdit(self.centralwidget)
        self.textSearch.setGeometry(QtCore.QRect(30, 260, 231, 181))
        self.textSearch.setObjectName("textSearch")
        self.labelSearch = QtWidgets.QLabel(self.centralwidget)
        self.labelSearch.setGeometry(QtCore.QRect(40, 220, 151, 31))
        self.labelSearch.setObjectName("labelSearch")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(330, 260, 271, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        Database.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Database)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 639, 25))
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
        self.action.setItemText(0, _translate("Database", "delete"))
        self.action.setItemText(1, _translate("Database", "update"))
        self.action.setItemText(2, _translate("Database", "insert"))
        self.actLabel.setText(_translate("Database", "Choose table and action to do:"))
        self.genData.setText(_translate("Database", "Generate random data to database!"))
        self.labelSearch.setText(_translate("Database", "Full-text search"))
        self.pushButton_2.setText(_translate("Database", "Find specified cargo -->"))

