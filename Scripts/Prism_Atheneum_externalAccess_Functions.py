# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2021 Richard Frangenberg
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


import os
import platform
import logging
import json

try:
    #from PySide2.QtCore import *
    #from PySide2.QtGui import *
    #from PySide2.QtWidgets import *
    
    from qtpy.QtCore import *
    from qtpy.QtGui import *
    from qtpy.QtWidgets import *

    psVersion = 2
except:
    from PySide.QtCore import *
    from PySide.QtGui import *


    psVersion = 1

if psVersion == 1:
    import SceneBrowser_ui
else:
    import Atheneum_ui_ps2 as Atheneum_ui
from qtpy import QtCore, QtGui, QtWidgets#

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

logger = logging.getLogger(__name__)

class Prism_Atheneum_externalAccess_Functions(QWidget):
    def __init__(self, core, plugin, refresh=True):
        #self.setupUi(self)
        self.pages = []
        self.core = core
        self.plugin = plugin
        self.core.registerCallback(
            "projectBrowser_loadUI", self.projectBrowser_loadUI, plugin=self.plugin
        )
        
        self.core.registerCallback(
            "onStateManagerOpen", self.onStateManagerOpen, plugin=self.plugin
        )
        self.core.registerCallback(
            "onStateManagerClose", self.onStateManagerClose, plugin=self.plugin
        )
        
        self.core.registerCallback(
            "prePlayblast", self.prePlayblast, plugin=self.plugin
        )
        self.core.registerCallback(
            "onStateStartup", self.onStateStartup, plugin=self, priority=40
        )
        
        self.core.registerCallback(
            "sm_export_updateUi", self.sm_export_updateUi, plugin=self, priority=40
        )
        
    def sm_export_updateUi(self, origin):
        pass
        
    @err_catcher(name=__name__)
    
    def refreshUI(self):
        pass
    
    def getAutobackPath(self, origin):
        autobackpath = ""
        if platform.system() == "Windows":
            autobackpath = os.path.join(
                self.core.getWindowsDocumentsPath(), "Atheneum"
            )

        fileStr = "Atheneum Scene File ("
        for i in self.sceneFormats:
            fileStr += "*%s " % i

        fileStr += ")"

        return autobackpath, fileStr

    @err_catcher(name=__name__)
    def copySceneFile(self, origin, origFile, targetPath, mode="copy"):
        pass
        
    def projectBrowser_loadUI(self, origin):
        if self.core.appPlugin.pluginName != "Standalone4":
            #psMenu = QMenu("LibraryR8")
            #psAction = QAction("Connect", origin)
            #psAction.triggered.connect(lambda: self.refresh("","","asset"))
            #psMenu.addAction(psAction)
            #origin.menuTools.addSeparator()
            #origin.menuTools.addMenu(psMenu)

            self.libTab = atheneum(
                core=self.core, refresh=False
            )
            origin.tbw_project.addTab(self.libTab,"Atheneum") 
            
        for cls in self.plugin.__class__.__mro__:  # Перебираем классы от текущего до object
            if hasattr(cls, "PB_loadUI") and cls != self.__class__:
                cls.PB_loadUI(self.plugin, origin)


    def onStateManagerOpen(self, origin):
        #origin.b_createPlayblast
        for cls in self.plugin.__class__.__mro__:  # Перебираем классы от текущего до object
            if hasattr(cls, "SM_Open") and cls != self.__class__:
                cls.SM_Open(self.plugin, origin)
                
    def onStateManagerClose(self, origin):
        for cls in self.plugin.__class__.__mro__:  # Перебираем классы от текущего до object
            if hasattr(cls, "SM_Close") and cls != self.__class__:
                cls.SM_Close(self.plugin, origin)

    def prePlayblast(self, **kwargs):
        origin = kwargs.get("state", None)
        for cls in self.plugin.__class__.__mro__:  # Перебираем классы от текущего до object
           if hasattr(cls, "SM_preBlast") and cls != self.__class__:
               cls.SM_preBlast(self.plugin, origin)
                

    def onStateStartup(self, origin):
        for cls in self.plugin.__class__.__mro__:  # Перебираем классы от текущего до object
            if hasattr(cls, "SM_Startup") and cls != self.__class__:
                cls.SM_Startup(self.plugin, origin)
                
        # if self.core.appPlugin.pluginName == "Maya":
            # if state.className == "Playblast":

                # self.new_groupbox = QGroupBox("Настройки")  # Создаем QGroupBox
                # self.new_layout = QVBoxLayout(self.new_groupbox)  # Лэйаут для QGroupBox
                # self.new_groupbox.setLayout(self.new_layout)  # Устанавливаем лэйаут

                # Создаем виджет с чекбоксом и лейблом
                # self.w_textured = QWidget()
                # self.lo_textured = QHBoxLayout()
                # self.lo_textured.setContentsMargins(9, 0, 9, 0)
                # self.w_textured.setLayout(self.lo_textured)

                # self.l_textured = QLabel("Textured Viewport:")
                # spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding)
                # self.chb_textured = QCheckBox()
                # self.chb_textured.setChecked(False)

                # self.lo_textured.addWidget(self.l_textured)
                # self.lo_textured.addSpacerItem(spacer)
                # self.lo_textured.addWidget(self.chb_textured)

                # self.new_layout.addWidget(self.w_textured)  # Добавляем в QGroupBox

                # Добавляем QGroupBox в основной лэйаут
                # origin.verticalLayout.addWidget(self.new_groupbox)


    #def prePlayblast(self, origin):
    #    print("---------------------------------------")

             
    def entered(self, prevTab=None, navData=None):
        import EntityWidget

        self.w_entities = EntityWidget.EntityWidget(core=self.core, refresh=False)
        self.splitter_5.insertWidget(0, self.w_entities)
    def rf(self):
        pass
class atheneum(QWidget, Atheneum_ui.Ui_w_Atheneum):
    def __init__(self, core, importState=None, refresh=True):
        QWidget.__init__(self)
        #self.path = "c:/work/testP2.0_library"
        #import EntityWidget
        self.core = core
        self.pages = []
        #self.core.parentWindow(self)
        self.entityPreviewWidth = 107
        self.entityPreviewHeight = 60
        #self.core.entities.refreshOmittedEntities()
        self.setupUi(self)

        self.core.callback(name="onAtheneumWidgetCreated", args=[self])
        self.tw_versions.doubleClicked.connect(self.asset_import) 
        self.cb_lib.currentIndexChanged.connect(self.libselect)
        self.at_path = self.refreshIntegrations()
        
        self.cb_lib.addItems(self.at_path)
        #for key, value in libList.items():
        
        #    self.cb_lib.addItem(key)
        #    self.cb_lib.setItemData(0, value)

    def refreshIntegrations(self):
        integrations = self.core.integration.getIntegrations()
        if "Atheneum" in integrations:
            afPath = integrations["Atheneum"]
        else:
            afPath = ""
        return afPath

        
    def refreshUI(self):
        pass
        
    def libselect(self):
        #selected_index = self.cb_lib.currentIndex()
        data = self.cb_lib.currentText()
        self.refresh(data,"","asset")
        return data
        
    def refresh(self, path,arg,type=None,current=""):

        self.tw_versions.clearContents()
        #self.tw_versions.setRowCount(0)
        #self.tw_versions.removeRow(0)
        #self.tw_versions.setItem(0, 0, QtWidgets.QTableWidgetItem())
        
        iconPath = os.path.join(
            self.core.prismRoot, "Scripts", "UserInterfacesPrism", "asset.png"
        )
        self.assetIcon = self.core.media.getColoredIcon(iconPath)

        iconPath = os.path.join(
            self.core.prismRoot, "Scripts", "UserInterfacesPrism", "folder.png"
        )
        self.folderIcon = self.core.media.getColoredIcon(iconPath)        

        if type=="asset":
            self.tw_assets.clear()
            self.tw_identifier.clear()
     
            #path = os.path.join(path, "03_Production", "Assets") #P2.0
            step = ["03_Workflow","03_Production"]
            for step_one in step:
                
                as_path = os.path.join(path, step_one, "Assets") #P1.0

                if os.path.exists(as_path):
                    assets_list = os.listdir(as_path)
                    for i in assets_list:
                        parrent = QtWidgets.QTreeWidgetItem([i])
                        self.tw_assets.addTopLevelItem(parrent)
                        if os.path.exists(os.path.join(as_path,i,"Export")):
                            parrent.setIcon(0, self.assetIcon)
                        else:
                            parrent.setIcon(0, self.folderIcon)
                            ccount = 0
                            for ci in os.listdir(os.path.join(as_path,i)):
                                child = QtWidgets.QTreeWidgetItem(parrent,[ci])
                                child.setText(ccount,ci)
                                data = {}
                                data["paths"] = path
                                data["asset"] = ci
                                data["type"] = "asset"
                                data["asset_path"] = ci
                                #child.setData(0, Qt.UserRole, ci)
                                child.setData(0, Qt.UserRole, data)
                                parrent.addChild(child)
                                ccount+=1
                                self.refreshAssetItem(child)
                                #path = os.path.join(path, ci)
                                
                    self.tw_assets.itemClicked.connect(lambda x,e="",b_path=as_path: self.onItemClicked(x,e,"product",b_path))

            
        elif type=="product":
            self.tw_identifier.clear()
            path = os.path.join(path, "Export")
            if os.path.exists(path):
                assets_list = os.listdir(path)
                for i in assets_list:
                    parrent = QtWidgets.QTreeWidgetItem([i])
                    data = {}
                    data["asset"] = i
                    parrent.setData(0, Qt.UserRole, data)
                    self.tw_identifier.addTopLevelItem(parrent)
                    self.atr="versions"
                    #self.pt=arg
                #self.tw_identifier.itemClicked.connect(self.onItemClicked)
                self.tw_identifier.itemClicked.connect(lambda x,e="": self.onItemClicked(x,e,"versions",path))
        elif type=="versions":
           
            self.tw_versions.clearContents()
            self.tw_versions.setRowCount(0)
            path = os.path.join(current, arg)
            if os.path.exists(path):
                assets_list = os.listdir(path)
                #self.tw_versions.setRowCount(len(assets_list)-1)
                rowPosition = 0
                for i,(name) in enumerate(assets_list):
                    if not "." in name:
                        #folderPath = os.path.join(path, name) #P2.0
                        folderPath = os.path.join(path, name,"centimeter") #P1.0
                        if not os.path.exists(folderPath):
                            folderPath = os.path.join(path, name)
                        ext = self.getExt(folderPath)

                        if ext:
                            self.tw_versions.setRowCount(rowPosition+1)
                            data = self.getData(folderPath)
                            if "pver" in data:
                                self.tw_versions.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(name)))
                            else:
                                self.tw_versions.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(data["version"])))
                            self.tw_versions.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(data["comment"])))
                            self.tw_versions.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(ext[1])))
                            self.tw_versions.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(str(data["user"])))
                            self.tw_versions.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(str(data["date"])))
                            self.tw_versions.setItem(rowPosition, 5, QtWidgets.QTableWidgetItem(str(path)))
                            
                            self.tw_versions.setColumnHidden(5, False)
                            rowPosition+=1
                        self.as_info.setText("test")
                #self.tw_versions.doubleClicked.connect(lambda x,e="": self.asset_import(x,e,arg,path))


    @err_catcher(name=__name__)
    def refreshAssetItem(self, item):
        item.takeChildren()

        #path = data["paths"][0]
        #path = ""
        item.takeChildren()
        data = item.data(0, Qt.UserRole)
        path = data["paths"][0]
        pm = self.core.entities.getEntityPreview(data)
        if not pm:
            pm = self.core.media.emptyPrvPixmap
        w_entity = QWidget()
        lo_entity = QHBoxLayout()
        lo_entity.setContentsMargins(0, 0, 0, 0)
        w_entity.setLayout(lo_entity)
        l_preview = QLabel()
        l_label = QLabel(os.path.basename(path))
        l_label = QLabel(item.text(0))
        lo_entity.addWidget(l_preview)
        lo_entity.addWidget(l_label)
        lo_entity.addStretch()

        # prvPath = "C:\\work\\testP2.0_library\\00_Pipeline\\Assetinfo\\test_asset_preview.jpg"
        # if os.path.exists(prvPath):
            # imgmap = QPixmap(prvPath)
            # child.setPixmap(imgmap)


        pmap = self.core.media.scalePixmap(pm, self.entityPreviewWidth, self.entityPreviewHeight, fitIntoBounds=False, crop=True)
        l_preview.setPixmap(pmap)

        self.tw_assets.setItemWidget(item, 0, w_entity)

        item.setText(0, "123")


            
    def onItemClicked(self, it, col, arg,current=""):

        name = it.data(0, Qt.UserRole)
        if not name:
            name = it.text(col)
        if it.parent():
            path = os.path.join(current,it.parent().text(0),name["asset"])
        else:
            path = os.path.join(current,name["asset"])
        self.refresh(path,name["asset"],arg,current)

    def asset_import(self, it):
        row = it.row()
        #    column = mi.column()

        path = os.path.join(self.tw_versions.item(row, 5).text(),self.tw_versions.item(row, 0).text())
        name = self.getExt(path)[0]
        fullPath = os.path.join(self.tw_versions.item(row, 5).text(),self.tw_versions.item(row, 0).text(),"centimeter",name)
        soft = self.core.appPlugin.pluginName
        if soft == "Cinema":
            self.ImportCinema(fullPath)
        elif soft == "Maya":
            self.ImportMaya(fullPath)
        elif soft == "Houdini":
            self.ImportHoudini(fullPath)            
        elif  soft == "Standalone":
            self.ImportStdl(fullPath)  



    # def asset_import1(self, it, col, arg,current=""):
        # path = os.path.join(current,self.tw_versions.item(it.row(), 0).text())
        # name = self.getExt(path)[0]
        # fullPath = os.path.join(current,self.tw_versions.item(it.row(), 0).text(),"centimeter",name)
        # soft = self.core.appPlugin.pluginName
        # if soft == "Cinema":
            # self.ImportCinema(fullPath)
        # elif soft == "Maya":
            # self.ImportMaya(fullPath)
        # elif soft == "Houdini":
            # self.ImportHoudini(fullPath)            
        # elif  soft == "Standalone":
            # self.ImportStdl(fullPath)  
    
    def getData(self, path):
        ifyml = os.path.join(path.replace("\centimeter",""),"versioninfo.yml")
        if os.path.exists(os.path.join(path,"versioninfo.json")):
            f_path = os.path.join(path,"versioninfo.json")
            f = open(f_path)
            data = json.load(f)
            f.close()
        elif os.path.exists(ifyml):
            data = {}
            f = open(ifyml)
            with open(ifyml) as f:
                for l in f:
                    if 'Version' in l:
                        data["version"] = l.split(": ")[1]
                    elif "Created" in l:
                        data["user"] = l.split(": ")[1]
                    elif "Creation" in l:
                        data["date"] = l.split(": ")[1]
                    data["comment"] = ""
                    data["pver"] = "1"
            f.close


        else:
            data = {}
            
        return data
        
    def getExt(self, path):
        blacklistExt = [".txt", ".ini", ".yml", ".json", ".xgen"]
        pone = os.path.join(path.replace("\centimeter",""),"versioninfo.yml")
        if os.path.exists(os.path.join(path,"versioninfo.json")) or os.path.exists(pone):

            if os.path.exists(pone) and not "\centimeter" in path:
                assets_list = os.listdir(os.path.join(path,"centimeter"))
            else:
                assets_list = os.listdir(path)
            for i in assets_list:
                if "." in i:
                    if i.split(".")[1] not in blacklistExt:
                        return i, i.split(".")[1]
            return None
        else:
            return None
    
            
            
    def ImportCinema(self, file):
        import c4d
        from c4d import documents, plugins
        doc = documents.GetActiveDocument()
        doc.StartUndo()

        flags = c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS | c4d.SCENEFILTER_MERGESCENE # Merge objects and materials
        c4d.documents.MergeDocument(doc, file, flags) # Merge asset to active project
        c4d.EventAdd() # Refresh Cinema 4D
        doc.EndUndo() # Stop recording undos
        
    def ImportMaya(self, file):
        pass
    def ImportHoudini(self, file):
        pass
    def ImportHoudini(self, file):
        pass
    def ImportStdl(self, file):
        print(file)
    def getSelectedContext(self):
        pass
        
    def setupUi1(self):
        #QtWidgets.QVBoxLayout
        self.HLayout = QtWidgets.QHBoxLayout()
        tree = QTreeWidget()
        tree.setColumnCount(2)
        tree.setHeaderLabels(["Name", "Type"])

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        self.VLayout = QtWidgets.QVBoxLayout()
        self.VLayout.setObjectName("VLayout")
        self.VLayout.addStretch(1)
        #self.VLayout.addWidget(okButton)
        #self.VLayout.addWidget(cancelButton)
        self.VLayout.addWidget(tree)
        

        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(self.VLayout)

        self.setLayout(vbox)
        self.setFixedWidth(80)

    def entered(self, prevTab=None, navData=None):
        pass

 