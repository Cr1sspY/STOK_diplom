import sqlite3
import sys
import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSlot

emp_id = 0


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
        self.ui.get_order()
        self.ui.add_ord_btn.clicked.connect(self.add_order)
        self.ui.upd_ord_btn.clicked.connect(self.get_order)
        self.ui.get_wh()
        self.ui.get_client()
        self.ui.get_service()
        self.ui.del_serv_btn.clicked.connect(self.delete_service)
        self.ui.save_serv_btn.clicked.connect(self.save_service)
        self.ui.get_history()

        if position == 'Администратор':
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.label_hist.hide()
            self.ui.label_emp.hide()
        elif position == 'Техник':
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.del_serv_btn.hide()
            self.ui.save_serv_btn.hide()
            self.ui.del_empl_btn.hide()
            self.ui.save_empl_btn.hide()
            self.ui.history_table.hide()
            self.ui.empl_table.hide()

    def exit(self):
        self.close()
        Auth()

    def get_order(self):
        self.ui.order_table.clear()
        rec = self.db.get_order()
        self.ui.order_table.setColumnCount(11)
        self.ui.order_table.setRowCount(len(rec))
        self.ui.order_table.setHorizontalHeaderLabels(['ID Заказа', 'Клиент', 'Услуга', 'Стоимость услуги, руб.',
                                                       'Комплектующая', 'Стоимость комплектующей, руб.',
                                                       'Сумма заказа, руб.', 'Статус', 'Дата заказа', 'Время заказа',
                                                       'Сотрудник'])
        for i, order in enumerate(rec):
            for x, field in enumerate(order):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.order_table.setItem(i, x, item)
        self.ui.order_table.resizeColumnsToContents()

    def add_order(self):
        add = 'order'
        win = Add(add)

    def get_wh(self):
        self.ui.wh_table.clear()
        rec = self.db.get_wh()
        self.ui.wh_table.setColumnCount(5)
        self.ui.wh_table.setRowCount(len(rec))
        self.ui.wh_table.setHorizontalHeaderLabels(['ID Комплектующей', 'Тип', 'Наименование', 'Количество, шт.',
                                                    'Стоимость, руб.'])
        for i, wh in enumerate(rec):
            for x, field in enumerate(wh):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.wh_table.setItem(i, x, item)
        self.ui.wh_table.resizeColumnsToContents()

    def get_client(self):
        self.ui.client_table.clear()
        rec = self.db.get_client()
        self.ui.client_table.setColumnCount(4)
        self.ui.client_table.setRowCount(len(rec))
        self.ui.client_table.setHorizontalHeaderLabels(['ID Клиента', 'Название', 'Номер телефона', 'Почта'])
        for i, client in enumerate(rec):
            for x, field in enumerate(client):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.client_table.setItem(i, x, item)
        self.ui.client_table.resizeColumnsToContents()

    def get_service(self):
        self.ui.service_table.clear()
        rec = self.db.get_service()
        self.ui.service_table.setColumnCount(3)
        self.ui.service_table.setRowCount(len(rec))
        self.ui.service_table.setHorizontalHeaderLabels(['ID Услуги', 'Услуга', 'Стоимость'])

        for i, service in enumerate(rec):
            for x, field in enumerate(service):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.service_table.setItem(i, x, item)
        self.ui.service_table.resizeColumnsToContents()

    def delete_service(self):
        selectedrow = self.ui.service_table.currentRow()
        rowcount = self.ui.service_table.rowCount()
        colcount = self.ui.service_table.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        elif selectedrow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        else:
            for col in range(1, colcount):
                self.ui.service_table.setItem(selectedrow, col, QTableWidgetItem(''))
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
                tmp.append(self.service_table.item(row, col).text())
            data.append(tmp)
        return data

    def get_history(self):
        self.ui.history_table.clear()
        rec = self.db.get_history()
        self.ui.history_table.setColumnCount(4)
        self.ui.history_table.setRowCount(len(rec))
        self.ui.history_table.setHorizontalHeaderLabels(['ID входа', 'Пользователь', 'Дата входа', 'Время входа'])

        for i, history in enumerate(rec):
            for x, field in enumerate(history):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.history_table.setItem(i, x, item)
        self.ui.history_table.resizeColumnsToContents()


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
            surname, name, second_name, position, emp_id = data[0]
            full_name = surname + ' ' + name[0] + '.' + second_name[0] + '.'
            main_win = MainWindow(position, full_name)
            date_enter = datetime.datetime.now()
            date_req = str(date_enter.strftime("%d.%m.%Y"))
            time_req = str(date_enter.strftime("%H:%M"))
            self.db.insert_log(emp_id, date_req, time_req)
            main_win.setWindowTitle('Станция техобслуживания компьютеров')

    def hide_pas(self):
        if self.hide_password:
            self.ui.password.setEchoMode(QLineEdit.Normal)
            self.hide_password = False
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)
            self.hide_password = True


class Add(QWidget):
    def __init__(self, add, parent=None):
        super(Add, self).__init__(parent)
        self.db = Database()
        self.ui = uic.loadUi("forms/add.ui", self)
        self.setWindowIcon(QIcon("images/logo.png"))
        self.ui.setWindowTitle('Добавление')
        self.ui.show()
        if add == 'order':
            self.ui.stackedWidget.setCurrentIndex(0)

        self.build_combobox_client()
        self.build_combobox_service()
        self.build_serv_cost()
        self.build_combobox_kompl()
        self.build_kompl_cost()
        self.ui.usluga_box.currentIndexChanged.connect(self.update_serv_cost)
        self.ui.usluga_box.currentIndexChanged.connect(self.update_sum)
        self.update_serv_cost()
        self.ui.kompl_box.currentIndexChanged.connect(self.update_kompl_cost)
        self.ui.kompl_box.currentIndexChanged.connect(self.update_sum)
        self.update_kompl_cost()
        self.update_sum()
        self.ui.btn_add_order.clicked.connect(self.add_order)

    def build_combobox_client(self):
        clients = self.db.get_client_cb()
        self.client_box.clear()
        if self.client_box is not None:
            self.client_box.addItems(clients)

    def build_combobox_service(self):
        services = self.db.get_service_cb()
        self.usluga_box.clear()
        if self.usluga_box is not None:
            self.usluga_box.addItems(services)

    def build_serv_cost(self):
        self.usl_cost.clear()
        self.ui.usl_cost.setText(str(self.db.get_serv_c(self.ui.usluga_box.currentText())))
        self.usl_cost.update()
        print()

    def build_combobox_kompl(self):
        kompls = self.db.get_kompl_cb()
        self.kompl_box.clear()
        if self.kompl_box is not None:
            self.kompl_box.addItems(kompls)

    def build_kompl_cost(self):
        self.kompl_cost.clear()
        self.ui.kompl_cost.setText(str(self.db.get_kompl_c(self.ui.kompl_box.currentText())))
        self.kompl_cost.update()
        print()

    def update_serv_cost(self):
        service = self.ui.usluga_box.currentText()
        self.ui.usl_cost.setText(str(self.db.get_serv_c(service)[0][0]))

    def update_kompl_cost(self):
        kompl = self.ui.kompl_box.currentText()
        self.ui.kompl_cost.setText(str(self.db.get_kompl_c(kompl)[0][0]))

    def update_sum(self):
        service_cost = self.ui.usl_cost.text()
        kompl_cost = self.ui.kompl_cost.text()
        summary = int(service_cost) + int(kompl_cost)
        self.ui.summary.setText(str(summary))

    def add_order(self):
        client = self.ui.client_box.currentText()
        client_id = int(str(self.db.get_client_id(client))[1:-2])
        print(client_id)
        service = self.ui.usluga_box.currentText()
        service_cost = self.ui.usl_cost.text()
        kompl = self.ui.kompl_box.currentText()
        kompl_cost = self.ui.kompl_cost.text()
        summary = int(service_cost) + int(kompl_cost)
        self.db.add_order(service, client_id, service_cost, kompl, kompl_cost, summary, emp_id)


class Database:
    def __init__(self):
        self.con = sqlite3.connect('stokdb.db')

    def get_auth_info(self, log, pas):
        cur = self.con.cursor()
        cur.execute(f'SELECT surname, name, second_name, position, emp_id FROM employee WHERE login="{log}" and password="{pas}"')
        data = cur.fetchall()
        cur.close()

        if data:
            return data
        else:
            return False

    def insert_log(self, id, enter_date, enter_time):
        cur = self.con.cursor()
        cur.execute(f"INSERT INTO history VALUES (NULL, ?, ?, ?);", (id, enter_date, enter_time))
        self.con.commit()
        cur.close()

    def get_order(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM order1")
        return cursor.fetchall()

    def get_client_cb(self):
        clients = []
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `cl_name` FROM client")
        rows = cursor.fetchall()

        for i in rows:
            clients.append(str(i)[2:-3])
        return clients

    def get_service_cb(self):
        services = []
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `serv_name` FROM service")
        rows = cursor.fetchall()

        for i in rows:
            services.append(str(i)[2:-3])
        return services

    def get_serv_c(self, service):
        cur = self.con.cursor()
        cur.execute(f'SELECT serv_cost FROM service WHERE serv_name="{service}"')
        serv_c = cur.fetchall()
        cur.close()
        return serv_c

    def get_kompl_cb(self):
        kompls = []
        cursor = self.con.cursor()
        cursor.execute(f"SELECT comp_name FROM component")
        rows = cursor.fetchall()

        for i in rows:
            kompls.append(str(i)[2:-3])
        return kompls

    def get_kompl_c(self, kompl):
        cur = self.con.cursor()
        cur.execute(f'SELECT comp_cost FROM component WHERE comp_name="{kompl}"')
        kompl_c = cur.fetchall()
        cur.close()
        return kompl_c

    def get_client_id(self, name):
        cur = self.con.cursor()
        cur.execute(f'SELECT cl_id FROM client WHERE cl_name="{name}"')
        cl_id = cur.fetchone()
        cur.close()
        print(cl_id)
        return cl_id

    def add_order(self, service, client, serv_cost, kompl, kompl_cost, summ, emp_id):
        now = datetime.datetime.now()
        times = now.strftime("%H:%M")
        date = now.strftime("%d.%m.20%y")
        id = 1
        try:
            cur = self.con.cursor()
            cur.execute("""INSERT INTO order1 VALUES (NULL,?,?,?,?,?,?,?,?,?,?)""", (client, service,
                                                                                    serv_cost, kompl, kompl_cost, summ,
                                                                                     "Новый заказ", date, times, emp_id))
            self.con.commit()
            cur.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def get_wh(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM component")
        return cursor.fetchall()

    def get_client(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM client")
        return cursor.fetchall()

    def get_service(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM service")
        return cursor.fetchall()

    def delete_service(self, id):
        cur = self.con.cursor()
        cur.execute(f'DELETE from service WHERE serv_id="{id}"')
        self.con.commit()
        cur.close()

    def update_service(self, id, name, cost):
        id = int(id)
        cur = self.con.cursor()
        cur.execute(f'UPDATE service set serv_name="{name}", serv_cost="{cost}" WHERE serv_id="{id}"')
        self.con.commit()
        cur.close()

    def get_history(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM history")
        return cursor.fetchall()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Auth()

    app.exec()