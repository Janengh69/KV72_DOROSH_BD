import psycopg2 as ps
from configparser import ConfigParser
from view import Ui_Database
from PyQt5 import QtCore, QtGui, QtWidgets

#TODO mvc model

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
	def __init__(self):
		conn = None
		try:
			params = self.config('config.ini')
			conn = ps.connect(**params)
			cursor = conn.cursor()
			cursor.execute('SELECT barcode from cargo')
			db = cursor.fetchall()
			print(db)
			cursor.close()
		except(Exception, ps.DatabaseError) as error:
			print(error)
		finally:
			if conn is not None:
				conn.close()
				print('connection closed')



if __name__ == '__main__':
	db = Database()
	import sys

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_Database()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())