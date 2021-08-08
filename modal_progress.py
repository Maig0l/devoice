# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modal_progress.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(409, 83)
        Dialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 0, 0, 1, 1)
        self.btn_stop = QtWidgets.QPushButton(Dialog)
        self.btn_stop.setObjectName("btn_stop")
        self.gridLayout.addWidget(self.btn_stop, 0, 1, 1, 1)
        self.lbl_status = QtWidgets.QLabel(Dialog)
        self.lbl_status.setObjectName("lbl_status")
        self.gridLayout.addWidget(self.lbl_status, 1, 0, 1, 1)
        self.btn_open = QtWidgets.QPushButton(Dialog)
        self.btn_open.setObjectName("btn_open")
        self.gridLayout.addWidget(self.btn_open, 1, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Separating"))
        self.btn_stop.setText(_translate("Dialog", "Cancel"))
        self.lbl_status.setText(_translate("Dialog", "Status..."))
        self.btn_open.setText(_translate("Dialog", "Open"))

