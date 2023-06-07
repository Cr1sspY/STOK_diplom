import sqlite3
import sys
import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSlot


class MainWindow(QMainWindow):
    def __init__(self, position, full_name, parent=None):
        super().__init__(parent)
        self.db = Database()
        self.ui = uic.loadUi("forms/main.ui", self)
        self.setWindowIcon(QIcon("images/logo.png"))
        self.ui.show()
        self.ui.label_fio.setText(full_name)
        self.ui.label_pos.setText(position)
        self.ui.exit_btn.clicked.connect(self.exit)
        self.get_service()
        self.ui.del_serv_btn.clicked.connect(self.delete_service)
        self.ui.save_serv_btn.clicked.connect(self.save_service)

        if position == 'Администратор':
            self.ui.stackedWidget.setCurrentIndex(0)
        elif position == 'Продавец':
            self.ui.stackedWidget.setCurrentIndex(1)

    def exit(self):
        self.close()
        Auth()

    def get_service(self):
        self.ui.service_table.clear()
        rec = self.db.get_service()
        self.ui.service_table.setRowCount(len(rec)+1)
        self.ui.service_table.setHorizontalHeaderLabels(['ID Услуги', 'Услуга', 'Стоимость'])

        for i, service in enumerate(rec):
            for x, field in enumerate(service):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.service_table.setItem(i, x, item)

    def delete_service(self):
        SelectedRow = self.ui.service_table.currentRow()
        rowcount = self.ui.service_table.rowCount()
        colcount = self.ui.service_table.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        else:
            for col in range(0, colcount):
                self.ui.service_table.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.ui.service_table.model().index(-1, -1)
            self.ui.service_table.setCurrentIndex(ix)

    def save_service(self):
        data = self.get_service_tbl()
        for string in data:
            if string[1] != '':                     # если название услуги есть, то обновляем данные
                self.db.update_service(string[0], string[1], string[2])
            else:                                   # если названия услуги нет, то удаляем эту строку
                self.db.delete_service(string[0])
        self.get_service()

    def get_service_tbl(self):
        rows = self.ui.service_table.rowCount()     # получаем кол-во строк таблицы
        cols = self.ui.service_table.columnCount()  # получаем кол-во столбцов таблицы
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.ui.service_table.item(row, col).text())
            data.append(tmp)
        return data


class Auth(QDialog):
    def __init__(self, parent=None):
        super(Auth, self).__init__(parent)
        self.db = Database()
        self.ui = uic.loadUi("forms/auth.ui", self)
        self.setWindowIcon(QIcon("images/logo.png"))
        self.ui.setWindowTitle('Авторизация')
        self.ui.show()
        self.enter_btn.clicked.connect(self.auth)
        self.sh_pw_btn.clicked.connect(self.hide_pas)
        self.hide_password = True

    def auth(self):
        log = self.ui.login.text()
        pas = self.ui.password.text()
        data = self.db.get_auth_info(log, pas)
        if data:
            self.ui.hide()
            surname, name, second_name, position = data[0]
            full_name = surname + ' ' + name[0] + '.' + second_name[0] + '.'
            main_win = MainWindow(position, full_name)
            main_win.setWindowTitle('Станция техобслуживания компьютеров')

    def hide_pas(self):
        if self.hide_password:
            self.ui.password.setEchoMode(QLineEdit.Normal)
            self.hide_password = False
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)
            self.hide_password = True


class Database:
    def __init__(self):
        self.con = sqlite3.connect('stokdb.db')

    def get_auth_info(self, log, pas):
        cur = self.con.cursor()
        cur.execute(f'SELECT surname, name, second_name, position FROM employee WHERE login="{log}" and password="{pas}"')
        data = cur.fetchall()
        cur.close()

        if data:
            return data
        else:
            return False

    def get_service(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM service")
        return cursor.fetchall()

    def delete_service(self):
        cur = self.db.cursor()
        cur.execute(f'DELETE from service WHERE serv_id="{id}"')
        self.db.commit()
        cur.close()

    def update_service(self, id, name, cost):
        id = int(id)
        cur = self.con.cursor()
        cur.execute(f'UPDATE service set serv_name="{name}", serv_cost="{cost}" WHERE serv_id="{id}"')
        self.con.commit()
        cur.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Auth()

    app.exec()