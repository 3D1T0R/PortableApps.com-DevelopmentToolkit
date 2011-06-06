# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frontend/guiqt/ui/frontend.ui'
#
#      by: pyside-uic 0.2.9 running on PySide 1.0.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.nav = QtGui.QWidget(self.centralwidget)
        self.nav.setStyleSheet("#nav{background:#202429 url(:/headerbar.png) no-repeat}\n"
"QLabel{color:rgba(255,255,255,51);font-size:10px}\n"
"QPushButton{border:none;background:none;font-weight:bold;color:#fff;padding:10px}\n"
"QPushButton:!enabled{color:#707070}\n"
"QPushButton:checked{color:#ff8000}\n"
"#nav_options,#nav_about{padding:0;height:14px;font-size:11px;font-weight:normal;color:#ccc}\n"
"#nav_options:checked,#nav_about:checked{color:#ff8000}")
        self.nav.setObjectName("nav")
        self.nav_layout = QtGui.QHBoxLayout(self.nav)
        self.nav_layout.setSpacing(10)
        self.nav_layout.setContentsMargins(80, -1, -1, -1)
        self.nav_layout.setObjectName("nav_layout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.nav_layout.addItem(spacerItem)
        self.nav_start = QtGui.QPushButton(self.nav)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nav_start.sizePolicy().hasHeightForWidth())
        self.nav_start.setSizePolicy(sizePolicy)
        self.nav_start.setCursor(QtCore.Qt.PointingHandCursor)
        self.nav_start.setFocusPolicy(QtCore.Qt.TabFocus)
        self.nav_start.setCheckable(True)
        self.nav_start.setChecked(True)
        self.nav_start.setObjectName("nav_start")
        self.nav_layout.addWidget(self.nav_start)
        self.nav_arrow_1 = QtGui.QLabel(self.nav)
        self.nav_arrow_1.setObjectName("nav_arrow_1")
        self.nav_layout.addWidget(self.nav_arrow_1)
        self.nav_details = QtGui.QPushButton(self.nav)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nav_details.sizePolicy().hasHeightForWidth())
        self.nav_details.setSizePolicy(sizePolicy)
        self.nav_details.setCursor(QtCore.Qt.PointingHandCursor)
        self.nav_details.setFocusPolicy(QtCore.Qt.TabFocus)
        self.nav_details.setCheckable(True)
        self.nav_details.setObjectName("nav_details")
        self.nav_layout.addWidget(self.nav_details)
        self.nav_arrow_2 = QtGui.QLabel(self.nav)
        self.nav_arrow_2.setObjectName("nav_arrow_2")
        self.nav_layout.addWidget(self.nav_arrow_2)
        self.nav_launcher = QtGui.QPushButton(self.nav)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nav_launcher.sizePolicy().hasHeightForWidth())
        self.nav_launcher.setSizePolicy(sizePolicy)
        self.nav_launcher.setCursor(QtCore.Qt.PointingHandCursor)
        self.nav_launcher.setFocusPolicy(QtCore.Qt.TabFocus)
        self.nav_launcher.setCheckable(True)
        self.nav_launcher.setObjectName("nav_launcher")
        self.nav_layout.addWidget(self.nav_launcher)
        self.nav_arrow_3 = QtGui.QLabel(self.nav)
        self.nav_arrow_3.setObjectName("nav_arrow_3")
        self.nav_layout.addWidget(self.nav_arrow_3)
        self.nav_compact = QtGui.QPushButton(self.nav)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nav_compact.sizePolicy().hasHeightForWidth())
        self.nav_compact.setSizePolicy(sizePolicy)
        self.nav_compact.setCursor(QtCore.Qt.PointingHandCursor)
        self.nav_compact.setFocusPolicy(QtCore.Qt.TabFocus)
        self.nav_compact.setCheckable(True)
        self.nav_compact.setObjectName("nav_compact")
        self.nav_layout.addWidget(self.nav_compact)
        self.nav_arrow_4 = QtGui.QLabel(self.nav)
        self.nav_arrow_4.setObjectName("nav_arrow_4")
        self.nav_layout.addWidget(self.nav_arrow_4)
        self.nav_test = QtGui.QPushButton(self.nav)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nav_test.sizePolicy().hasHeightForWidth())
        self.nav_test.setSizePolicy(sizePolicy)
        self.nav_test.setCursor(QtCore.Qt.PointingHandCursor)
        self.nav_test.setFocusPolicy(QtCore.Qt.TabFocus)
        self.nav_test.setCheckable(True)
        self.nav_test.setObjectName("nav_test")
        self.nav_layout.addWidget(self.nav_test)
        self.nav_arrow_5 = QtGui.QLabel(self.nav)
        self.nav_arrow_5.setObjectName("nav_arrow_5")
        self.nav_layout.addWidget(self.nav_arrow_5)
        self.nav_publish = QtGui.QPushButton(self.nav)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nav_publish.sizePolicy().hasHeightForWidth())
        self.nav_publish.setSizePolicy(sizePolicy)
        self.nav_publish.setCursor(QtCore.Qt.PointingHandCursor)
        self.nav_publish.setFocusPolicy(QtCore.Qt.TabFocus)
        self.nav_publish.setCheckable(True)
        self.nav_publish.setObjectName("nav_publish")
        self.nav_layout.addWidget(self.nav_publish)
        self.nav_smallbox = QtGui.QVBoxLayout()
        self.nav_smallbox.setSpacing(6)
        self.nav_smallbox.setContentsMargins(72, -1, -1, -1)
        self.nav_smallbox.setObjectName("nav_smallbox")
        self.nav_options = QtGui.QPushButton(self.nav)
        self.nav_options.setCursor(QtCore.Qt.PointingHandCursor)
        self.nav_options.setFocusPolicy(QtCore.Qt.TabFocus)
        self.nav_options.setCheckable(True)
        self.nav_options.setObjectName("nav_options")
        self.nav_smallbox.addWidget(self.nav_options)
        self.nav_about = QtGui.QPushButton(self.nav)
        self.nav_about.setCursor(QtCore.Qt.PointingHandCursor)
        self.nav_about.setFocusPolicy(QtCore.Qt.TabFocus)
        self.nav_about.setCheckable(True)
        self.nav_about.setObjectName("nav_about")
        self.nav_smallbox.addWidget(self.nav_about)
        self.nav_layout.addLayout(self.nav_smallbox)
        self.verticalLayout.addWidget(self.nav)
        self.pages = QtGui.QStackedWidget(self.centralwidget)
        self.pages.setObjectName("pages")
        self.verticalLayout.addWidget(self.pages)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "PortableApps.com Development Toolkit", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_start.setText(QtGui.QApplication.translate("MainWindow", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_arrow_1.setText(QtGui.QApplication.translate("MainWindow", "▶", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_details.setText(QtGui.QApplication.translate("MainWindow", "Details", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_arrow_2.setText(QtGui.QApplication.translate("MainWindow", "▶", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_launcher.setText(QtGui.QApplication.translate("MainWindow", "Launcher", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_arrow_3.setText(QtGui.QApplication.translate("MainWindow", "▶", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_compact.setText(QtGui.QApplication.translate("MainWindow", "Compact", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_arrow_4.setText(QtGui.QApplication.translate("MainWindow", "▶", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_test.setText(QtGui.QApplication.translate("MainWindow", "Test", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_arrow_5.setText(QtGui.QApplication.translate("MainWindow", "▶", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_publish.setText(QtGui.QApplication.translate("MainWindow", "Publish", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_options.setText(QtGui.QApplication.translate("MainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_about.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
