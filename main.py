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
        self.ui.del_ord_btn.clicked.connect(self.delete_order)
        self.ui.save_ord_btn.clicked.connect(self.save_order)
        self.ui.get_wh()
        self.ui.add_wh_btn.clicked.connect(self.add_wh)
        self.ui.upd_wh_btn.clicked.connect(self.get_wh)
        self.ui.del_wh_btn.clicked.connect(self.delete_wh)
        self.ui.save_wh_btn.clicked.connect(self.save_wh)
        self.ui.get_client()
        self.ui.add_client_btn.clicked.connect(self.add_client)
        self.ui.upd_client_btn.clicked.connect(self.get_client)
        self.ui.del_cl_btn.clicked.connect(self.delete_client)
        self.ui.save_cl_btn.clicked.connect(self.save_client)
        self.ui.get_service()
        self.ui.del_serv_btn.clicked.connect(self.delete_service)
        self.ui.add_serv_btn.clicked.connect(self.add_service)
        self.ui.upd_serv_btn.clicked.connect(self.get_service)
        self.ui.save_serv_btn.clicked.connect(self.save_service)
        self.ui.get_history()
        self.ui.get_emp()
        self.ui.del_empl_btn.clicked.connect(self.delete_emp)
        self.ui.add_emp_btn.clicked.connect(self.add_emp)
        self.ui.upd_emp_btn.clicked.connect(self.get_emp)
        self.ui.save_empl_btn.clicked.connect(self.save_emp)

        if position == 'Администратор':
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.label_hist.hide()
            self.ui.label_emp.hide()
        elif position == 'Техник':
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.del_serv_btn.hide()
            self.ui.save_serv_btn.hide()
            self.ui.add_serv_btn.hide()
            self.ui.upd_serv_btn.hide()
            self.ui.del_empl_btn.hide()
            self.ui.save_empl_btn.hide()
            self.ui.empl_table.hide()
            self.ui.add_emp_btn.hide()
            self.ui.upd_emp_btn.hide()
            self.ui.history_table.hide()

    def exit(self):
        self.close()
        Auth()

    # Функции, связанные с ЗАКАЗАМИ

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
        self.order_table.setSortingEnabled(True)

    def add_order(self):
        add = 'order'
        win = Add(add)

    def delete_order(self):
        selectedrow = self.ui.order_table.currentRow()
        rowcount = self.ui.order_table.rowCount()
        colcount = self.ui.order_table.columnCount()

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
                self.ui.order_table.setItem(selectedrow, col, QTableWidgetItem(''))
            ix = self.ui.order_table.model().index(-1, -1)
            self.ui.order_table.setCurrentIndex(ix)

    def save_order(self):
        data = self.get_order_tbl()
        for string in data:
            if string[1] != '':                     # если название услуги есть, то обновляем данные
                self.db.update_order(string[0], string[7])
            else:                                   # если названия услуги нет, то удаляем эту строку
                self.db.delete_order(string[0])
        self.get_order()

    def get_order_tbl(self):
        rows = self.ui.order_table.rowCount()     # получаем кол-во строк таблицы
        cols = self.ui.order_table.columnCount()  # получаем кол-во столбцов таблицы
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.order_table.item(row, col).text())
            data.append(tmp)
        return data

    # Функции, связанные с КОМПЛЕКТУЮЩИМИ

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
        self.wh_table.setSortingEnabled(True)

    def add_wh(self):
        add = 'wh'
        win = Add(add)

    def delete_wh(self):
        selectedrow = self.ui.wh_table.currentRow()
        rowcount = self.ui.wh_table.rowCount()
        colcount = self.ui.wh_table.columnCount()

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
                self.ui.wh_table.setItem(selectedrow, col, QTableWidgetItem(''))
            ix = self.ui.wh_table.model().index(-1, -1)
            self.ui.wh_table.setCurrentIndex(ix)

    def save_wh(self):
        data = self.get_wh_tbl()
        for string in data:
            if string[1] != '':     # если название услуги есть, то обновляем данные
                self.db.update_wh(string[0], string[1], string[2], string[3], string[4])
            else:                   # если названия услуги нет, то удаляем эту строку
                self.db.delete_wh(string[0])
        self.get_wh()

    def get_wh_tbl(self):
        rows = self.ui.wh_table.rowCount()     # получаем кол-во строк таблицы
        cols = self.ui.wh_table.columnCount()  # получаем кол-во столбцов таблицы
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.wh_table.item(row, col).text())
            data.append(tmp)
        return data

    # Функции, связанные с КЛИЕНТАМИ

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
        self.client_table.setSortingEnabled(True)

    def add_client(self):
        add = 'client'
        win = Add(add)

    def delete_client(self):
        selectedrow = self.ui.client_table.currentRow()
        rowcount = self.ui.client_table.rowCount()
        colcount = self.ui.client_table.columnCount()

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
                self.ui.client_table.setItem(selectedrow, col, QTableWidgetItem(''))
            ix = self.ui.client_table.model().index(-1, -1)
            self.ui.client_table.setCurrentIndex(ix)

    def save_client(self):
        data = self.get_client_tbl()
        for string in data:
            if string[1] != '':     # если название услуги есть, то обновляем данные
                self.db.update_client(string[0], string[1], string[2], string[3])
            else:                   # если названия услуги нет, то удаляем эту строку
                self.db.delete_client(string[0])
        self.get_client()

    def get_client_tbl(self):
        rows = self.ui.client_table.rowCount()     # получаем кол-во строк таблицы
        cols = self.ui.client_table.columnCount()  # получаем кол-во столбцов таблицы
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.client_table.item(row, col).text())
            data.append(tmp)
        return data

    # Функции, связанные с УСЛУГАМИ

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
        self.service_table.setSortingEnabled(True)

    def add_service(self):
        add = 'serv'
        win = Add(add)

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

    # Функции, связанные с ИСТОРИЕЙ

    def get_history(self):
        self.ui.history_table.clear()
        rec = self.db.get_history()
        self.ui.history_table.setColumnCount(3)
        self.ui.history_table.setRowCount(len(rec))
        self.ui.history_table.setHorizontalHeaderLabels(['Пользователь', 'Дата входа', 'Время входа'])

        for i, history in enumerate(rec):
            for x, field in enumerate(history):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.history_table.setItem(i, x, item)
        self.ui.history_table.resizeColumnsToContents()
        self.history_table.setSortingEnabled(True)

    # Функции, связанные с СОТРУДНИКАМИ

    def get_emp(self):
        self.ui.empl_table.clear()
        rec = self.db.get_emp()
        self.ui.empl_table.setColumnCount(7)
        self.ui.empl_table.setRowCount(len(rec))
        self.ui.empl_table.setHorizontalHeaderLabels(['ID Сотрудника', 'Фамилия', 'Имя', 'Отчество', 'Должность',
                                                      'Логин', 'Пароль'])

        for i, service in enumerate(rec):
            for x, field in enumerate(service):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.empl_table.setItem(i, x, item)
        self.ui.empl_table.resizeColumnsToContents()
        self.empl_table.setSortingEnabled(True)

    def add_emp(self):
        add = 'emp'
        win = Add(add)

    def delete_emp(self):
        selectedrow = self.ui.empl_table.currentRow()
        rowcount = self.ui.empl_table.rowCount()
        colcount = self.ui.empl_table.columnCount()

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
                self.ui.empl_table.setItem(selectedrow, col, QTableWidgetItem(''))
            ix = self.ui.empl_table.model().index(-1, -1)
            self.ui.empl_table.setCurrentIndex(ix)

    def save_emp(self):
        data = self.get_emp_tbl()
        for string in data:
            if string[1] != '':                     # если название услуги есть, то обновляем данные
                self.db.update_emp(string[0], string[1], string[2], string[3], string[4], string[5], string[6])
            else:                                   # если названия услуги нет, то удаляем эту строку
                self.db.delete_emp(string[0])
        self.get_emp()

    def get_emp_tbl(self):
        rows = self.ui.empl_table.rowCount()     # получаем кол-во строк таблицы
        cols = self.ui.empl_table.columnCount()  # получаем кол-во столбцов таблицы
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.empl_table.item(row, col).text())
            data.append(tmp)
        return data


class Auth(QDialog):
    def __init__(self, parent=None):
        super(Auth, self).__init__(parent)
        self.db = Database()
        self.ui = uic.loadUi("forms/auth.ui", self)
        self.setWindowIcon(QIcon("images/logo.png"))
        self.ui.setWindowTitle('Авторизация — СТОК')
        self.ui.show()
        self.enter_btn.clicked.connect(self.auth)
        self.sh_pw_btn.clicked.connect(self.hide_pas)
        self.hide_password = True
        self.exit_btn.clicked.connect(self.exit)

    def auth(self):
        log = self.ui.login.text()
        pas = self.ui.password.text()
        data = self.db.get_auth_info(log, pas)
        if data:
            type = 'Успех!'
            text = 'Вы успешно вошли в систему.'
            self.mes_box(type, text)
            self.ui.hide()
            global emp_id
            surname, name, second_name, position, emp_id = data[0]
            full_name = surname + ' ' + name[0] + '.' + second_name[0] + '.'
            main_win = MainWindow(position, full_name)
            date_enter = datetime.datetime.now()
            date_req = str(date_enter.strftime("%d.%m.%Y"))
            time_req = str(date_enter.strftime("%H:%M"))
            self.db.insert_log(emp_id, date_req, time_req)
            main_win.setWindowTitle('Станция техобслуживания компьютеров')
        elif log == '' or pas == '':
            type = 'Ошибка'
            text = 'Поля не могут быть пустыми!'
            self.mes_box(type, text)
        else:
            type = 'Ошибка'
            text = 'Проверьте корректность введённых данных.'
            self.mes_box(type, text)

    def hide_pas(self):
        if self.hide_password:
            self.ui.password.setEchoMode(QLineEdit.Normal)
            self.hide_password = False
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)
            self.hide_password = True

    def mes_box(self, type, text):
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle(type)
        messagebox.setText(text)
        messagebox.setStandardButtons(QMessageBox.Ok)
        messagebox.show()

    def exit(self):
        sys.exit()


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
        elif add == 'wh':
            self.ui.stackedWidget.setCurrentIndex(1)
        elif add == 'client':
            self.ui.stackedWidget.setCurrentIndex(2)
        elif add == 'service':
            self.ui.stackedWidget.setCurrentIndex(3)
        elif add == 'emp':
            self.ui.stackedWidget.setCurrentIndex(4)

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
        self.ui.btn_add_wh.clicked.connect(self.add_wh)
        self.ui.btn_add_client.clicked.connect(self.add_client)
        self.ui.btn_add_serv.clicked.connect(self.add_service)
        self.ui.btn_add_emp.clicked.connect(self.add_emp)

    def mes_box(self, type, text):
        messagebox = QMessageBox(self)
        messagebox.setWindowTitle(type)
        messagebox.setText(text)
        messagebox.setStandardButtons(QMessageBox.Ok)
        messagebox.show()

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
        service = self.ui.usluga_box.currentText()
        service_id = int(str(self.db.get_service_id(service))[1:-2])
        service_cost = self.ui.usl_cost.text()
        kompl = self.ui.kompl_box.currentText()
        kompl_id = int(str(self.db.get_kompl_id(kompl))[1:-2])
        kompl_cost = self.ui.kompl_cost.text()
        summary = int(service_cost) + int(kompl_cost)
        self.db.add_order(service_id, client_id, service_cost, kompl_id, kompl_cost, summary, emp_id)
        type = 'Оформление заказа'
        text = 'Заказ успешно оформлен. Нажмите кнопку "Обновить".'
        self.mes_box(type, text)
        self.close()

    def add_wh(self):
        comp_type = self.ui.line_wh_type.text()
        name = self.ui.line_wh_name.text()
        qua = self.ui.spin_wh_qua.value()
        cost = self.ui.spin_wh_cost.value()
        self.db.add_wh(comp_type, name, qua, cost)
        type = 'Добавление на склад'
        text = 'Комплектующая успешно добавлена. Нажмите кнопку "Обновить".'
        self.mes_box(type, text)
        self.close()

    def add_client(self):
        name = self.ui.client_name_line.text()
        number = self.ui.phone_line.text()
        email = self.ui.email_line.text()
        self.db.add_client(name, number, email)
        type = 'Добавление клиента'
        text = 'Клиент успешно добавлен. Нажмите кнопку "Обновить".'
        self.mes_box(type, text)
        self.close()

    def add_service(self):
        name = self.ui.serv_name_line.text()
        cost = self.ui.serv_cost_box.value()
        self.db.add_service(name, cost)
        type = 'Добавление услуги'
        text = 'Услуга успешно добавлена. Нажмите кнопку "Обновить".'
        self.mes_box(type, text)
        self.close()

    def add_emp(self):
        surname = self.ui.emp_sur_line.text()
        name = self.ui.emp_name_line.text()
        second = self.ui.emp_sec_line.text()
        pos = self.ui.emp_pos_cb.currentText()
        log = self.ui.emp_log_line.text()
        pas = self.ui.emp_pas_line.text()
        self.db.add_emp(surname, name, second, pos, log, pas)
        type = 'Добавление сотрудника'
        text = 'Сотрудник успешно добавлен. Нажмите кнопку "Обновить".'
        self.mes_box(type, text)
        self.close()


class Database:
    def __init__(self):
        self.con = sqlite3.connect('stokdb.db')

    def get_auth_info(self, log, pas):
        cur = self.con.cursor()
        cur.execute(f'SELECT surname, name, second_name, position, emp_id FROM employee WHERE login="{log}"'
                    f' and password="{pas}"')
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

    # Функции, связанные с ЗАКАЗАМИ

    def get_order(self):
        orders = []
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM order1")
        data = cursor.fetchall()
        for i in data:
            list_data = list(i)
            for x, j in enumerate(i):
                if x == 1:
                    list_data[1] = str(self.get_name_client(j))[1:-1]
                if x == 2:
                    list_data[2] = str(self.get_name_service(j))[1:-1]
                if x == 4:
                    list_data[4] = str(self.get_name_komp(j))[1:-1]
                if x == 10:
                    list_data[10] = str(self.get_name_emp(j))[1:-1]
                else:
                    continue
                orders.append(list_data)
        return orders

    def get_name_client(self, id):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `cl_name` FROM client WHERE `cl_id`='{id}'")
        name = cursor.fetchone()
        return str(name)[1:-2]

    def get_name_service(self, id):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `serv_name` FROM service WHERE `serv_id`='{id}'")
        name = cursor.fetchone()
        return str(name)[1:-2]

    def get_name_emp(self, id):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `surname` FROM employee WHERE `emp_id`='{id}'")
        name = cursor.fetchone()
        return str(name)[1:-2]

    def get_name_komp(self, id):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `comp_name` FROM component WHERE `comp_id`='{id}'")
        name = cursor.fetchone()
        return str(name)[1:-2]

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
        return cl_id

    def get_service_id(self, name):
        cur = self.con.cursor()
        cur.execute(f'SELECT serv_id FROM service WHERE serv_name="{name}"')
        serv_id = cur.fetchone()
        cur.close()
        return serv_id

    def get_kompl_id(self, name):
        cur = self.con.cursor()
        cur.execute(f'SELECT comp_id FROM component WHERE comp_name="{name}"')
        kompl_id = cur.fetchone()
        cur.close()
        return kompl_id

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

    def delete_order(self, id):
        cur = self.con.cursor()
        cur.execute(f'DELETE from order1 WHERE ord_id="{id}"')
        self.con.commit()
        cur.close()

    def update_order(self, id, status):
        id = int(id)
        cur = self.con.cursor()
        cur.execute(f'UPDATE order1 set status="{status}" WHERE ord_id="{id}"')
        self.con.commit()
        cur.close()

    # Функции, связанные с КОМПЛЕКТУЮЩИМИ

    def get_wh(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM component")
        return cursor.fetchall()

    def add_wh(self, comp_type, name, qua, cost):
        id = 1
        try:
            cur = self.con.cursor()
            cur.execute("""INSERT INTO component VALUES (NULL,?,?,?,?)""", (comp_type, name, qua, cost))
            self.con.commit()
            cur.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def delete_wh(self, id):
        cur = self.con.cursor()
        cur.execute(f'DELETE from component WHERE comp_id="{id}"')
        self.con.commit()
        cur.close()

    def update_wh(self, id, type, name, qua, cost):
        id = int(id)
        cur = self.con.cursor()
        cur.execute(f'UPDATE component set comp_type="{type}", comp_name="{name}", quantity="{qua}", comp_cost="{cost}"'
                    f'WHERE comp_id="{id}"')
        self.con.commit()
        cur.close()

    # Функции, связанные с КЛИЕНТАМИ

    def get_client(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM client")
        return cursor.fetchall()

    def add_client(self, name, phone, email):
        id = 1
        try:
            cur = self.con.cursor()
            cur.execute("""INSERT INTO client VALUES (NULL,?,?,?)""", (name, phone, email))
            self.con.commit()
            cur.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def delete_client(self, id):
        cur = self.con.cursor()
        cur.execute(f'DELETE from client WHERE cl_id="{id}"')
        self.con.commit()
        cur.close()

    def update_client(self, id, name, phone, email):
        id = int(id)
        cur = self.con.cursor()
        cur.execute(f'UPDATE client set cl_name="{name}", ph_number="{phone}", email="{email}" WHERE cl_id="{id}"')
        self.con.commit()
        cur.close()

    # Функции, связанные с УСЛУГАМИ

    def get_service(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM service")
        return cursor.fetchall()

    def add_service(self, name, cost):
        id = 1
        try:
            cur = self.con.cursor()
            cur.execute("""INSERT INTO service VALUES (NULL,?,?)""", (name, cost))
            self.con.commit()
            cur.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

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

    # Функции, связанные с ИСТОРИЕЙ

    def get_history(self):
        emp = []
        cursor = self.con.cursor()
        cursor.execute(f"SELECT employee, enter_date, enter_time FROM history")
        data = cursor.fetchall()
        for i in data:
            list_data = list(i)
            for x, j in enumerate(i):
                if x == 0:
                    list_data[0] = str(self.get_login_emp(j))[1:-1]
                else:
                    continue
                emp.append(list_data)

        return emp

    def get_login_emp(self, id):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT `login` FROM employee WHERE `emp_id`='{id}'")
        name = cursor.fetchone()
        return str(name)[1:-2]

    # Функции, связанные с СОТРУДНИКАМИ

    def get_emp(self):
        cursor = self.con.cursor()
        cursor.execute(f"SELECT * FROM employee")
        return cursor.fetchall()

    def add_emp(self, surname, name, second_name, pos, log, pas):
        id = 1
        try:
            cur = self.con.cursor()
            cur.execute("""INSERT INTO employee VALUES (NULL,?,?,?,?,?,?)""", (surname, name, second_name, pos, log, pas))
            self.con.commit()
            cur.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def delete_emp(self, id):
        cur = self.con.cursor()
        cur.execute(f'DELETE from employee WHERE emp_id="{id}"')
        self.con.commit()
        cur.close()

    def update_emp(self, id, surname, name, second_name, pos, log, pas):
        id = int(id)
        cur = self.con.cursor()
        cur.execute(f'UPDATE employee set surname="{surname}", name="{name}", second_name="{second_name}",'
                    f'position="{pos}", login="{log}", password="{pas}" WHERE emp_id="{id}"')
        self.con.commit()
        cur.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Auth()

    app.exec()