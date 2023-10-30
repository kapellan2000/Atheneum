# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SceneBrowser.ui'
#
# Created: Wed Jun 23 16:34:09 2021
#      by: pyside2-uic @pyside_tools_VERSION@ running on PySide2 2.0.0~alpha0
#

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_w_Atheneum(object):
    def setupUi(self, w_Atheneum):
        w_Atheneum.setObjectName("w_Atheneum")
        w_Atheneum.resize(1294, 696)
        #self.verticalLayout_01 = QtWidgets.QVBoxLayout(w_Atheneum)
        #self.verticalLayout_01.setObjectName("verticalLayout_01")
        
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(w_Atheneum)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.splitter = QtWidgets.QSplitter(w_Atheneum)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        
        self.w_assets = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_assets.sizePolicy().hasHeightForWidth())
        self.w_assets.setSizePolicy(sizePolicy)
        self.w_assets.setObjectName("w_assets")
        self.verticalLayout_01 = QtWidgets.QVBoxLayout(self.w_assets)
        self.verticalLayout_01.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_01.setObjectName("verticalLayout_01")
        self.l_assets = QtWidgets.QLabel(self.w_assets)
        self.l_assets.setObjectName("l_assets")
        self.verticalLayout_01.addWidget(self.l_assets)
        self.tw_assets = QtWidgets.QTreeWidget(self.w_assets)
        self.tw_assets.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tw_assets.setIndentation(10)
        self.tw_assets.setObjectName("tw_assets")
        self.tw_assets.headerItem().setText(0, "1")
        self.tw_assets.header().setVisible(False)
        self.verticalLayout_01.addWidget(self.tw_assets) 
        




        self.l_layer = QtWidgets.QLabel("Library:")
        self.cb_lib = QtWidgets.QComboBox()
        self.verticalLayout_01.addWidget(self.l_layer) 
        self.verticalLayout_01.addWidget(self.cb_lib) 
        #self.cb_lib.addItems(['One', 'Two', 'Three', 'Four'])
        
        
        
        
        self.w_tasks = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_tasks.sizePolicy().hasHeightForWidth())
        self.w_tasks.setSizePolicy(sizePolicy)
        self.w_tasks.setObjectName("w_tasks")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.w_tasks)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.l_identifier = QtWidgets.QLabel(self.w_tasks)
        self.l_identifier.setObjectName("l_identifier")
        self.verticalLayout_3.addWidget(self.l_identifier)
        self.tw_identifier = QtWidgets.QTreeWidget(self.w_tasks)
        self.tw_identifier.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tw_identifier.setIndentation(10)
        self.tw_identifier.setObjectName("tw_identifier")
        self.tw_identifier.headerItem().setText(0, "1")
        self.tw_identifier.header().setVisible(False)
        self.verticalLayout_3.addWidget(self.tw_identifier)
        
        self.w_versions = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(30)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_versions.sizePolicy().hasHeightForWidth())
        self.w_versions.setSizePolicy(sizePolicy)
        self.w_versions.setObjectName("w_versions")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.w_versions)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.w_version = QtWidgets.QWidget(self.w_versions)
        self.w_version.setObjectName("w_version")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.w_version)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.l_version = QtWidgets.QLabel(self.w_version)
        self.l_version.setObjectName("l_version")
        self.horizontalLayout.addWidget(self.l_version)
        self.l_versionRight = QtWidgets.QLabel(self.w_version)
        self.l_versionRight.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.l_versionRight.setText("")
        self.l_versionRight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.l_versionRight.setObjectName("l_versionRight")
        self.horizontalLayout.addWidget(self.l_versionRight)
        self.verticalLayout_2.addWidget(self.w_version)
        self.tw_versions = QtWidgets.QTableWidget(self.w_versions)
        self.tw_versions.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tw_versions.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_versions.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tw_versions.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tw_versions.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tw_versions.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tw_versions.setShowGrid(False)
        self.tw_versions.setObjectName("tw_versions")
        self.tw_versions.setColumnCount(6)
        self.tw_versions.setRowCount(0)
        self.tw_versions.setHorizontalHeaderLabels(["Version", "Comment", "Type","User","Date"])
        self.tw_versions.horizontalHeader().setCascadingSectionResizes(False)
        self.tw_versions.horizontalHeader().setHighlightSections(False)
        self.tw_versions.horizontalHeader().setMinimumSectionSize(0)
        self.tw_versions.verticalHeader().setVisible(False)
        #self.verticalLayout_01
        self.verticalLayout_2.addWidget(self.tw_versions)
        self.verticalLayout_4.addWidget(self.splitter)
        
        self.as_info = QtWidgets.QLabel("")
        self.verticalLayout_2.addWidget(self.as_info)

        self.retranslateUi(w_Atheneum)
        #QtCore.QMetaObject.connectSlotsByName(w_Atheneum)
    def retranslateUi(self, w_Atheneum):
        w_Atheneum.setWindowTitle(QtWidgets.QApplication.translate("w_Atheneum", "Atheneum", None, -1))
        self.l_assets.setText(QtWidgets.QApplication.translate("w_Atheneum", "Assets:", None, -1))
        self.l_identifier.setText(QtWidgets.QApplication.translate("w_Atheneum", "Products:", None, -1))
        self.l_version.setText(QtWidgets.QApplication.translate("w_Atheneum", "Versions:", None, -1))
        self.tw_versions.setSortingEnabled(True)

