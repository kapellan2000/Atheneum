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
import shutil

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

from PrismUtils.Decorators import err_catcher as err_catcher


logger = logging.getLogger(__name__)


class Prism_Atheneum_Prism(object):
    def __init__(self, core, plugin):
        self.pages = []
        self.core = core
        self.plugin = plugin
        
        self.core.registerCallback("onProductBrowserOpen", self.onProductBrowserOpen, plugin=self.plugin)
        self.core.registerCallback("onStateManagerOpen", self.onStateManagerOpen, plugin=self.plugin)
        #self.core.registerCallback("postPublish", self.postPublish, plugin=self.plugin)
        self.core.registerCallback("postExport", self.postExport, plugin=self.plugin)
        
        self.core.registerCallback("openPBFileContextMenu", self.openPBFileContextMenu, plugin=self.plugin)
        self.core.registerCallback("getStateMenu", self.getStateMenu, plugin=self.plugin)




    @err_catcher(name=__name__)
    def getStateMenu(self, *args):
        origint = args[0]
        createMenu = args[1]

        act = createMenu.addAction("Duplica")

        def on_duplicate_clicked():
            selStateData = [[s, None] for s in origint.getSelectedStates()]
            if not selStateData:
                return

            origint.appendChildStates(selStateData[-1][0], selStateData)

            stateData = {"states": []}
            for idx, i in enumerate(selStateData):
                path = i[0].ui.getStateProps().get("filepath")  # без лишней скобки
                sm = self.core.getStateManager()
                if sm and path:
                    sm.importFile(path)

        act.triggered.connect(on_duplicate_clicked)



    @err_catcher(name=__name__)
    def openPBFileContextMenu(self, *args):
        
        origint = args[0]
        rcmenu = args[1]
        filepath = args[2]

        actions = rcmenu.actions()
        localAct = QAction(origint.core.tr("Copy to local"), origint)

        for i, action in enumerate(actions):
            if action.text() == "Copy to global":
                if self.core.useLocalFiles:
                    localAct.setEnabled(True)
                else:
                    localAct.setEnabled(False)
                if i + 1 < len(actions):
                    rcmenu.insertAction(actions[i + 1], localAct)
                else:
                    rcmenu.addAction(localAct)
                break
        
        localAct.triggered.connect(lambda: self.copyToLocal(os.path.normpath(filepath), origint))
        

    @err_catcher(name=__name__)
    def copyToLocal(self, localPath, origint):
        dstPath = localPath.replace(self.core.projectPath, self.core.localProjectPath)

        if os.path.isdir(localPath):
            if os.path.exists(dstPath):
                for i in os.walk(dstPath):
                    if i[2] != []:
                        msg = self.core.tr("Found existing files in the local directory. Copy to local was canceled.")
                        self.core.popup(msg)
                        return

                shutil.rmtree(dstPath)

            shutil.copytree(dstPath, localPath)

            try:
                shutil.rmtree(localPath)
            except:
                msg = self.core.tr("Could not delete the global file. Probably it is used by another process.")
                self.core.popup(msg)

        else:
            if not os.path.exists(os.path.dirname(dstPath)):
                os.makedirs(os.path.dirname(dstPath))

            self.core.copySceneFile(localPath, dstPath)
            origint.refreshScenefilesThreaded()



        
    def onStateManagerOpen(self, *args):
        print("PPPPPP")
        # Create preview on publlish >>>
        if not args:
            return

        state_manager = args[0]
        self.StateManagerAddBtn(state_manager)
        
        if not hasattr(state_manager, "_is_publish_wrapped"):
            original_publish = state_manager.publish

            def wrapped_publish(*args, **kwargs):
                #checked = [x for x in state_manager.states if x.checkState(0) == Qt.Checked]
                checked = False
                count = 0
                for i in state_manager.states:

                    print(i.ui.objectName())
                    #if hasattr(i.ui, 'property'):
                    #    print(i.ui.property('name'))
                    if i.checkState(0) == Qt.Checked:
                        count+=1
                        if str(i.ui.objectName()) != "wg_Export":
                            count+=1 
                print("COunt ", count)
                if count == 1:
                    checked = True
                print("checked ", checked)
                
                if checked and state_manager.previewImg == None:
                    state_manager.getPreview()
                return original_publish(*args, **kwargs)

            state_manager.publish = wrapped_publish
            state_manager._is_publish_wrapped = True
        # Create preview on publlish <<<

    #def postPublish(self, *args, **kwargs):
     #   print("@@@> ", args)
      #  print("@-@-@> ", kwargs)

    def postExport(self, **kwargs):
        scenefile_path = kwargs['scenefile'].split(".")[0]+"preview.jpg"
        output_path = kwargs['outputpath'].split(".")[0]+"preview.jpg"
        if os.path.exists(scenefile_path):
            shutil.copyfile(scenefile_path, output_path)
        
    def onProductBrowserOpen(self, *args):
        widget = args[0].tw_versions  
        original_mouse_press = widget.mousePressEvent
        original_mouse_move = widget.mouseMoveEvent

        def wrappedMousePressEvent(event):
            self._click_pos = event.pos()

            if event.button() == Qt.RightButton:
                # просто передаём событие дальше, не трогаем
                if original_mouse_press:
                    original_mouse_press(event)
                return

            index = widget.indexAt(event.pos())
            if hasattr(self, 'detailWin') and self.detailWin is not None and self.detailWin.isVisible():
                self.detailWin.close()
                self.detailWin = None

            if index.isValid():
                row = index.row()
                first_col_index = index.sibling(row, 0)
                model = index.model()

                if model is not None:
                    data = model.data(first_col_index, Qt.UserRole)
                    print(data)
                    for i in data:
                        print(">> ", i, "- ", data[i])
                        
                    required_keys = ["path", "asset", "task", "version"]
                    if isinstance(data, dict) and all(k in data for k in required_keys):
                        
                        prvPath = (
                            data["path"] + "\\" +
                            data["asset"] + "_" +
                            data["product"] + "_" +
                            data["version"] + "preview.jpg"
                        )
                        print(prvPath)
                        if os.path.exists(prvPath):
                            self.detailWin = QFrame()
                            ss = getattr(self.core.appPlugin, "getFrameStyleSheet", lambda x: "")(self)
                            self.detailWin.setStyleSheet(
                                ss + """ .QFrame{ border: 2px solid rgb(100,100,100);} """
                            )

                            self.core.parentWindow(self.detailWin)
                            winwidth = 320
                            winheight = 10
                            VBox = QVBoxLayout()

                            imgmap = self.core.media.getPixmapFromPath(prvPath)
                            l_prv = QLabel()
                            l_prv.setPixmap(imgmap)
                            l_prv.setStyleSheet("border: 1px solid rgb(100,100,100);")
                            VBox.addWidget(l_prv)

                            w_info = QWidget()
                            GridL = QGridLayout()
                            GridL.setColumnStretch(1, 1)
                            w_info.setLayout(GridL)
                            GridL.setContentsMargins(0, 0, 0, 0)
                            VBox.addWidget(w_info)

                            self.detailWin.setLayout(VBox)
                            self.detailWin.setWindowFlags(
                                Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SplashScreen
                            )
                            self.detailWin.setAttribute(Qt.WA_ShowWithoutActivating)
                            self.detailWin.setGeometry(0, 0, winwidth, winheight)
                            self.detailWin.move(QCursor.pos().x() + 20, QCursor.pos().y())
                            self.detailWin.show()

                            def close_on_click(event):
                                if self.detailWin:
                                    self.detailWin.close()
                                    self.detailWin = None

                            self.detailWin.mousePressEvent = close_on_click
                    else:
                        print(f"[Atheneum] Пропущено: отсутствуют ключи в data — {data}")
                else:
                    print("[Atheneum] Нет model у index")
            else:
                print("[Atheneum] Невалидный index")

            if original_mouse_press:
                original_mouse_press(event)

        def wrappedMouseMoveEvent(event):
            if hasattr(self, '_click_pos') and (event.pos() - self._click_pos).manhattanLength() < 5:
                return  

            if hasattr(self, 'detailWin') and self.detailWin is not None and self.detailWin.isVisible():
                self.detailWin.close()
                self.detailWin = None

            if original_mouse_move:
                original_mouse_move(event)

        # Назначаем обработчики
        widget.mousePressEvent = wrappedMousePressEvent
        widget.mouseMoveEvent = wrappedMouseMoveEvent
            # preview in ProductBrowser <<<