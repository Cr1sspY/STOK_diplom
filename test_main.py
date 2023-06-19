import sys
from unittest import TestCase

from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from main import Add


class TestPush(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        self.window_order = Add('order')
        self.window_wh = Add('wh')
        self.window_client = Add('client')
        self.window_serv = Add('serv')
        self.window_emp = Add('emp')

    def test_push_order(self):
        btn_add = self.window_order.ui.btn_add_order
        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_push_wh(self):
        btn_add = self.window_wh.ui.btn_add_wh
        self.window_wh.ui.line_wh_type.setText("test")
        self.window_wh.ui.line_wh_name.setText("test")
        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_push_client(self):
        btn_add = self.window_wh.ui.btn_add_client
        self.window_client.ui.client_name_line.setText("test")
        self.window_client.ui.phone_line.setText("89999999999")
        self.window_client.ui.email_line.setText("test@test.ru")
        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_push_service(self):
        btn_add = self.window_serv.ui.btn_add_serv
        self.window_serv.ui.serv_name_line.setText("test")
        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)

    def test_push_employee(self):
        btn_add = self.window_wh.ui.btn_add_emp
        self.window_client.ui.emp_sur_line.setText("test")
        self.window_client.ui.emp_name_line.setText("test")
        self.window_client.ui.emp_sec_line.setText("test")
        self.window_client.ui.emp_log_line.setText("1")
        self.window_client.ui.emp_pas_line.setText("1")
        QTest.mouseClick(btn_add, QtCore.Qt.MouseButton.LeftButton)
