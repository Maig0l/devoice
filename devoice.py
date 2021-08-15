# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'devoice.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(458, 510)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.hbox_input = QtWidgets.QHBoxLayout()
        self.hbox_input.setObjectName("hbox_input")
        self.lbl_input = QtWidgets.QLabel(self.centralwidget)
        self.lbl_input.setObjectName("lbl_input")
        self.hbox_input.addWidget(self.lbl_input)
        self.line_input = QtWidgets.QLineEdit(self.centralwidget)
        self.line_input.setMinimumSize(QtCore.QSize(230, 0))
        self.line_input.setMouseTracking(True)
        self.line_input.setInputMask("")
        self.line_input.setText("")
        self.line_input.setFrame(True)
        self.line_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.line_input.setPlaceholderText("")
        self.line_input.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.line_input.setObjectName("line_input")
        self.hbox_input.addWidget(self.line_input)
        self.btn_inputOpen = QtWidgets.QPushButton(self.centralwidget)
        self.btn_inputOpen.setObjectName("btn_inputOpen")
        self.hbox_input.addWidget(self.btn_inputOpen)
        self.verticalLayout.addLayout(self.hbox_input)
        self.vbox_opts = QtWidgets.QVBoxLayout()
        self.vbox_opts.setObjectName("vbox_opts")
        self.lbl_opts = QtWidgets.QLabel(self.centralwidget)
        self.lbl_opts.setMaximumSize(QtCore.QSize(16777215, 29))
        self.lbl_opts.setObjectName("lbl_opts")
        self.vbox_opts.addWidget(self.lbl_opts)
        self.grp_model = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_model.setObjectName("grp_model")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.grp_model)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rad_debug = QtWidgets.QRadioButton(self.grp_model)
        self.rad_debug.setObjectName("rad_debug")
        self.horizontalLayout_3.addWidget(self.rad_debug)
        self.rad_demucs = QtWidgets.QRadioButton(self.grp_model)
        self.rad_demucs.setChecked(True)
        self.rad_demucs.setAutoExclusive(True)
        self.rad_demucs.setObjectName("rad_demucs")
        self.horizontalLayout_3.addWidget(self.rad_demucs)
        self.rad_spleeter = QtWidgets.QRadioButton(self.grp_model)
        self.rad_spleeter.setEnabled(False)
        self.rad_spleeter.setCheckable(True)
        self.rad_spleeter.setAutoExclusive(True)
        self.rad_spleeter.setObjectName("rad_spleeter")
        self.horizontalLayout_3.addWidget(self.rad_spleeter)
        self.vbox_opts.addWidget(self.grp_model)
        self.grp_stems = QtWidgets.QGroupBox(self.centralwidget)
        self.grp_stems.setObjectName("grp_stems")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.grp_stems)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rad_stems2 = QtWidgets.QRadioButton(self.grp_stems)
        self.rad_stems2.setEnabled(True)
        self.rad_stems2.setChecked(True)
        self.rad_stems2.setObjectName("rad_stems2")
        self.verticalLayout_3.addWidget(self.rad_stems2)
        self.rad_stems4 = QtWidgets.QRadioButton(self.grp_stems)
        self.rad_stems4.setObjectName("rad_stems4")
        self.verticalLayout_3.addWidget(self.rad_stems4)
        self.vbox_opts.addWidget(self.grp_stems)
        self.verticalLayout.addLayout(self.vbox_opts)
        self.hbox_outDir = QtWidgets.QHBoxLayout()
        self.hbox_outDir.setObjectName("hbox_outDir")
        self.lbl_outDir = QtWidgets.QLabel(self.centralwidget)
        self.lbl_outDir.setObjectName("lbl_outDir")
        self.hbox_outDir.addWidget(self.lbl_outDir)
        self.line_outDir = QtWidgets.QLineEdit(self.centralwidget)
        self.line_outDir.setMinimumSize(QtCore.QSize(276, 0))
        self.line_outDir.setObjectName("line_outDir")
        self.hbox_outDir.addWidget(self.line_outDir)
        self.btn_outOpen = QtWidgets.QPushButton(self.centralwidget)
        self.btn_outOpen.setObjectName("btn_outOpen")
        self.hbox_outDir.addWidget(self.btn_outOpen)
        self.verticalLayout.addLayout(self.hbox_outDir)
        self.btn_go = QtWidgets.QPushButton(self.centralwidget)
        self.btn_go.setObjectName("btn_go")
        self.verticalLayout.addWidget(self.btn_go)
        self.btn_stop = QtWidgets.QPushButton(self.centralwidget)
        self.btn_stop.setAutoDefault(False)
        self.btn_stop.setDefault(False)
        self.btn_stop.setFlat(False)
        self.btn_stop.setObjectName("btn_stop")
        self.verticalLayout.addWidget(self.btn_stop)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 458, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.act_openProgDialog = QtWidgets.QAction(MainWindow)
        self.act_openProgDialog.setObjectName("act_openProgDialog")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Devoice"))
        self.lbl_input.setText(_translate("MainWindow", "Input File:"))
        self.btn_inputOpen.setText(_translate("MainWindow", "Browse..."))
        self.lbl_opts.setText(_translate("MainWindow", "Separation options:"))
        self.grp_model.setTitle(_translate("MainWindow", "AI Model"))
        self.rad_debug.setText(_translate("MainWindow", "None (debug)"))
        self.rad_demucs.setText(_translate("MainWindow", "De&mucs"))
        self.rad_spleeter.setText(_translate("MainWindow", "Spleeter"))
        self.grp_stems.setTitle(_translate("MainWindow", "Number of stems"))
        self.rad_stems2.setText(_translate("MainWindow", "&2 Stems (Vocals, accompaniment)"))
        self.rad_stems4.setText(_translate("MainWindow", "&4 Stems (Vocals, drums, bass, others)"))
        self.lbl_outDir.setText(_translate("MainWindow", "Output Dir:"))
        self.btn_outOpen.setText(_translate("MainWindow", "Browse..."))
        self.btn_go.setText(_translate("MainWindow", "Devoice!"))
        self.btn_stop.setText(_translate("MainWindow", "Cancel"))
        self.act_openProgDialog.setText(_translate("MainWindow", "Open progress dialog"))

