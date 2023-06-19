import sys
from unittest import TestCase

from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from main import Add


class TestPush(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        self.window1 = Add()
        self.window2 = Add()

    def test_push_order(self):


    def test_push_wh(self):


    def test_push_client(self):


    def test_push_service(self):


    def test_push_employee(self):
