# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.canvas = QtWidgets.QWidget(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(10, 10, 451, 531))
        self.canvas.setObjectName("canvas")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(470, 10, 321, 241))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_grid = QtWidgets.QWidget()
        self.tab_grid.setObjectName("tab_grid")
        self.formLayoutWidget = QtWidgets.QWidget(self.tab_grid)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 311, 211))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.showGridLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.showGridLabel.setObjectName("showGridLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.showGridLabel)
        self.showGridCheckBox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.showGridCheckBox.setChecked(True)
        self.showGridCheckBox.setObjectName("showGridCheckBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.showGridCheckBox)
        self.gridSizeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.gridSizeLabel.setObjectName("gridSizeLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.gridSizeLabel)
        self.gridSizeSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.gridSizeSpinBox.setMinimum(1)
        self.gridSizeSpinBox.setProperty("value", 10)
        self.gridSizeSpinBox.setObjectName("gridSizeSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.gridSizeSpinBox)
        self.tabWidget.addTab(self.tab_grid, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setGeometry(QtCore.QRect(470, 260, 321, 281))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_import = QtWidgets.QWidget()
        self.tab_import.setObjectName("tab_import")
        self.label_input_filename = QtWidgets.QLabel(self.tab_import)
        self.label_input_filename.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label_input_filename.setObjectName("label_input_filename")
        self.input_json = QtWidgets.QLineEdit(self.tab_import)
        self.input_json.setGeometry(QtCore.QRect(60, 10, 171, 21))
        self.input_json.setObjectName("input_json")
        self.button_load_json = QtWidgets.QPushButton(self.tab_import)
        self.button_load_json.setGeometry(QtCore.QRect(240, 10, 75, 23))
        self.button_load_json.setObjectName("button_load_json")
        self.label_input_json = QtWidgets.QLabel(self.tab_import)
        self.label_input_json.setGeometry(QtCore.QRect(10, 50, 61, 16))
        self.label_input_json.setObjectName("label_input_json")
        self.text_imported_json = QtWidgets.QTextBrowser(self.tab_import)
        self.text_imported_json.setGeometry(QtCore.QRect(10, 70, 301, 181))
        self.text_imported_json.setObjectName("text_imported_json")
        self.tabWidget_2.addTab(self.tab_import, "")
        self.tab_export = QtWidgets.QWidget()
        self.tab_export.setObjectName("tab_export")
        self.text_exported_json = QtWidgets.QTextBrowser(self.tab_export)
        self.text_exported_json.setGeometry(QtCore.QRect(10, 70, 301, 181))
        self.text_exported_json.setObjectName("text_exported_json")
        self.label_output_json = QtWidgets.QLabel(self.tab_export)
        self.label_output_json.setGeometry(QtCore.QRect(10, 50, 61, 16))
        self.label_output_json.setObjectName("label_output_json")
        self.output_json = QtWidgets.QLineEdit(self.tab_export)
        self.output_json.setGeometry(QtCore.QRect(60, 10, 171, 21))
        self.output_json.setObjectName("output_json")
        self.button_save_json = QtWidgets.QPushButton(self.tab_export)
        self.button_save_json.setGeometry(QtCore.QRect(240, 10, 75, 23))
        self.button_save_json.setObjectName("button_save_json")
        self.label_output_filename = QtWidgets.QLabel(self.tab_export)
        self.label_output_filename.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label_output_filename.setObjectName("label_output_filename")
        self.tabWidget_2.addTab(self.tab_export, "")
        self.tab_json = QtWidgets.QWidget()
        self.tab_json.setObjectName("tab_json")
        self.text_current_json = QtWidgets.QTextBrowser(self.tab_json)
        self.text_current_json.setGeometry(QtCore.QRect(0, 30, 311, 221))
        self.text_current_json.setReadOnly(True)
        self.text_current_json.setAcceptRichText(False)
        self.text_current_json.setObjectName("text_current_json")
        self.label_current_json = QtWidgets.QLabel(self.tab_json)
        self.label_current_json.setGeometry(QtCore.QRect(0, 0, 121, 21))
        self.label_current_json.setObjectName("label_current_json")
        self.tabWidget_2.addTab(self.tab_json, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.showGridLabel.setText(_translate("MainWindow", "Show grid"))
        self.gridSizeLabel.setText(_translate("MainWindow", "Grid size"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_grid), _translate("MainWindow", "Grid"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.label_input_filename.setText(_translate("MainWindow", "Filename"))
        self.button_load_json.setText(_translate("MainWindow", "Load"))
        self.label_input_json.setText(_translate("MainWindow", "JSON input"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_import), _translate("MainWindow", "Import"))
        self.label_output_json.setText(_translate("MainWindow", "JSON output"))
        self.button_save_json.setText(_translate("MainWindow", "Save"))
        self.label_output_filename.setText(_translate("MainWindow", "Filename"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_export), _translate("MainWindow", "Export"))
        self.label_current_json.setText(_translate("MainWindow", "JSON for current canvas"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_json), _translate("MainWindow", "JSON"))

