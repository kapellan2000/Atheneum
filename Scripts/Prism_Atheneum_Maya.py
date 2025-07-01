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
import sys
import platform
import logging
import json
import inspect

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
from PrismUtils import PrismWidgets

logger = logging.getLogger(__name__)

#notes self.core.getPlugin("Deadline").deadlineSubmitJob(jobInfos, pluginInfos, arguments)

#if self.core.appPlugin.pluginName == "Maya":
#  self.core.plugins.monkeyPatch(self.core.appPlugin.sm_import_importToApp, self.sm_import_importToApp, self, force=True)

class Prism_Atheneum_Maya(object):
    def __init__(self, core, plugin):
        self.pages = []
        self.core = core
        self.plugin = plugin
        
        self.core.registerCallback(
            "onStateManagerOpen", self.onStateManagerOpenMa, plugin=self.plugin
        )
        self.core.registerCallback(
            "preImport", self.preImport, plugin=self.plugin
        )
        if self.core.appPlugin.pluginName == "Maya":
            import maya.cmds as cmds
            import maya.mel as mel
            self.cmds = cmds
            self.mel = mel
            
            import mayaUsd.lib as mayaUsdLib
            from pxr import Usd, UsdGeom

            self.mayaUsdLib = mayaUsdLib
            self.usd = Usd
            self.UsdGeom = UsdGeom
            
            self.hud_items = [
                ("Logo:", True),
                ("Shot Name:", True),
                ("Comment:", True),
                ("Frame:", True),
                ("Time Code:", True),
                ("Camera:", True)
            ]
            self.transform_node = "R8HUD"

            self.core.plugins.monkeyPatch(self.core.saveSceneInfo, self.saveSceneInfo, self, force=True)
            # self.core.registerCallback("onStateManagerShow", self.onStateManagerShow, plugin=self.plugin)
        

    def preImport(self, *args, **kwargs):
        #usd import 
        ext = os.path.splitext(kwargs["importfile"])[1]
        
        parts = kwargs["importfile"].split("\\")
        name = parts[parts.index("Export") - 1]
        XfOfs = "/root"
        if ext==".usd" or ext==".usda":
            pass

            file_path = self.cmds.file(q=True, sceneName=True)


            if file_path == "":
                self.core.showFileNotInProjectWarning()
                return
            if not self.core.fileInPipeline(file_path, validateFilename=False):
                self.core.showFileNotInProjectWarning()
                return
            else:
                #print(f"📁 Сцена сохранена: {file_path}")
                #print(f"📝 Имя файла: {os.path.basename(file_path)}")


                sel = self.cmds.ls(selection=True, long=True)
                if not sel:
                    create_stage = True
                else:

                    node_type = self.cmds.nodeType(sel[0])

                    if node_type == "transform":
                        children = self.cmds.listRelatives(sel[0], children=True, fullPath=True) or []
                        usd_shapes = [child for child in children if self.cmds.nodeType(child) == "mayaUsdProxyShape"]

                        if usd_shapes:
                            create_stage = False
                        else:
                            create_stage = True
                    elif node_type == "mayaUsdProxyShape":
                        create_stage = False
                    else:
                        create_stage = True
                action = 1
                if create_stage:
                    msg = QMessageBox(
                        QMessageBox.Question,
                        "Create Stage",
                        "⚠️No USD Stage selected. Do you want to create a new reference?",
                        QMessageBox.No,
                    )
                    msg.addButton("Yes", QMessageBox.YesRole)
                    msg.setParent(self.core.messageParent, Qt.Window)
                    action = msg.exec_()
                if action == 0:

                    # Загружаем плагин, если ещё не загружен
                    if not self.cmds.pluginInfo('mayaUsdPlugin', query=True, loaded=True):
                        self.cmds.loadPlugin('mayaUsdPlugin')


                    fileName = self.core.getCurrentFileName()
                    context = self.core.getScenefileData(fileName)

                    nameWin = PrismWidgets.CreateItem(
                        startText="USD_",
                        showTasks=True,
                        taskType="export",
                        core=self.core
                    )
                    self.core.parentWindow(nameWin)
                    nameWin.setWindowTitle("USD_Name")
                    nameWin.l_item.setText("Productname:")
                    nameWin.buttonBox.buttons()[0].setText("Ok")
                    nameWin.e_item.selectAll()
                    
                    comment_field = QtWidgets.QLineEdit()
                    comment_field.setPlaceholderText("Comment")
                    nameWin.layout().addWidget(comment_field)
                    
                    result = nameWin.exec_()
                    if result == 0:
                        return {"cancel": True}
                        
                    product = nameWin.e_item.text()
                    comment = comment_field.text()

                    #product = "usd"
                    extension=".usda"
                    framePadding = ""
                    publishComment=comment
                    version= ""
                    location="global"


                    #context['department'] = 'Usd'
                    #context['task'] = 'usd'

                    sData = self.core.products.generateProductPath(
                        entity=context,
                        task=product,
                        extension=extension,
                        framePadding=framePadding,
                        comment=publishComment,
                        version=version,
                        location=location,
                        returnDetails=True,
                    )



                    usd_file = sData["path"]

                    # Создаём transform и proxy shape
                    transform = self.cmds.createNode('transform', name='UsdStageRoot_' + product)
                    shape = self.cmds.createNode('mayaUsdProxyShape', name='UsdStageShape_' + product, parent=transform)

                    # Привязываем файл к shape
                    self.cmds.setAttr(f"{shape}.filePath", usd_file, type="string")
                    self.cmds.setAttr(f"{shape}.primPath", "/", type="string")

                    # Создаём новый USD Stage
                    stage = self.usd.Stage.CreateNew(usd_file)
                    group1 = self.UsdGeom.Xform.Define(stage, XfOfs)
                    infoPath = os.path.join(os.path.dirname(usd_file), "versioninfo.json")
                    os.makedirs(os.path.dirname(infoPath), exist_ok=True)
                    self.core.setConfig(configPath=infoPath, data=sData, updateNestedData=True)
                    
                elif action == 1:
                    shape = sel[0]
                    
                    usd_path = self.cmds.getAttr(f"{shape}.filePath")
                    if not usd_path:
                        raise RuntimeError("Выделенный shape не содержит путь к файлу.")
                    stage = self.usd.Stage.Open(usd_path)

                else :
                    return {"cancel": True}
                
                XfOfsTr = XfOfs+ "/XfTr" + name
                # Добавляем Xform /Group1/Group2
                group2 = self.UsdGeom.Xform.Define(stage, XfOfsTr)
                # Сохраняем изменения
                
                # Получаем прим /Xform/Xform (куда будет импорт)
                target_prim = stage.GetPrimAtPath(XfOfsTr)

                # Добавляем референс
                target_prim.GetReferences().AddReference(kwargs["importfile"])
                
                
                stage.GetRootLayer().Save()




                
                print("USD Stage создан и Xform добавлен.")
            
                
                
                
                back = {"cancel": True}
                
                
                
            #else:
            #    back = {"cancel": False}
            return back
        
    def StateManagerAddBtn(self, origin):
        if self.core.appPlugin.pluginName == "Maya":
            menu = origin.menuAbout
            for action in menu.actions():
                print(action.text())
            action_exists = any(action.text() == ">Restore connection" for action in menu.actions())

            if not action_exists:
                action_restore = menu.addAction(">Restore connection")
                action_restore_state = menu.addAction(">>Restore state + connectio")

                action_restore.triggered.connect(lambda: self.restore_state_and_connection(origin,"connect_only"))
                action_restore_state.triggered.connect(lambda: self.restore_state_and_connection(origin, "state_and_connect"))




    def restore_state_and_connection(self, origin, mode):
        scenePath = self.cmds.file(q=True, sn=True)
        infoPath = (
            os.path.splitext(scenePath)[0]
            + "versioninfo"
            + self.core.configs.getProjectExtension()
        )
        if os.path.exists(infoPath):
            sceneInfo = self.core.getConfig(configPath=infoPath)

        if not mode == "connect_only":
            all_states_str = sceneInfo['allStates']


            origin.loadStates(all_states_str)

            origin.showState()
            origin.activeList.clearFocus()
            origin.activeList.setFocus()


        PrismStates_str = sceneInfo['PrismStates'] 
        json_string = json.dumps(PrismStates_str)
        self.cmds.fileInfo("PrismStates", json_string)

        PrismImports_str = sceneInfo['PrismImports'] 
        json_string = json.dumps(PrismImports_str)
        self.cmds.fileInfo("PrismImports", json_string)
        
            
    def saveSceneInfo(self, filepath, details=None, preview=None, clean=True, replace=False):
        original = self.core
        details = details or {}
        if "username" not in details:
            details["username"] = original.username

        if "user" not in details:
            details["user"] = original.user

        doDeps = original.getConfig("globals", "track_dependencies", config="project")
        if doDeps == "always":
            deps = original.entities.getCurrentDependencies()
            details["dependencies"] = deps["dependencies"]
            details["externalFiles"] = deps["externalFiles"]

        if replace:
            sData = details
        else:
            sData = original.getScenefileData(filepath)
            if "project_name" in sData and original.fileInPipeline(filepath, validateFilename=False):
                del sData["project_name"]

            sData.update(details)

        if clean:
            keys = ["filename", "extension", "path", "paths", "task_path"]
            for key in keys:
                if key in sData:
                    del sData[key]
        sData['allStates'] = getattr(self.core.appPlugin, "sm_readStates", lambda x: None)(self)
        
        
        
        value = self.cmds.fileInfo("PrismStates", query=True)

        if value:
            sData['PrismStates'] = value[0]
        else:
            sData['PrismStates'] = ""
            
        value = self.cmds.fileInfo("PrismImports", query=True)

        if value:
            sData['PrismImports'] = value[0]
        else:
            sData['PrismImports'] = ""
    
        
        
        infoPath = original.getVersioninfoPath(filepath)
        original.setConfig(configPath=infoPath, data=sData, updateNestedData=not replace)
        if preview:
            original.core.entities.setScenePreview(filepath, preview)
            
        
    def PB_loadUI(self, origin):
        if self.core.appPlugin.pluginName != "Standalone":
            pass
            # psMenu = QMenu("LibraryR8999")
            # psAction = QAction("Connect", origin)

            # psAction.triggered.connect(lambda: self.refresh("","","asset"))
            # psMenu.addAction(psAction)
            # origin.menuTools.addSeparator()
            # origin.menuTools.addMenu(psMenu)
            #self.layout = QGridLayout()

    def load_Overlay(self, origin):
        
        #plugin_path = "C:/ProgramData/Prism2/plugins/Atheneum/Scripts/maya/OverlayTextNode.py"
        #if os.path.exists(plugin_path):
        #    self.cmds.loadPlugin(plugin_path)

        geo = "R8HUD"
        if self.cmds.objExists(geo):
            children = self.cmds.listRelatives(geo, children=True, fullPath=True)
            if children:
                self.cmds.delete(geo)


        plugin_path = "C:/ProgramData/Prism2/plugins/Atheneum/Scripts/maya/OverlayTextNode.py"
        plugin_name = os.path.basename(plugin_path)

        if not self.cmds.pluginInfo(plugin_name, query=True, loaded=True):

            if os.path.exists(plugin_path):
                self.cmds.loadPlugin(plugin_path)
        
        if not self.cmds.objExists(geo):
            transform_node = self.cmds.createNode("transform", name=geo)
        else:
            transform_node = geo

        if not self.cmds.objExists("R8HUD_Shape"):
            overlay_node = self.cmds.createNode("OverlayTextNode", name="R8HUD_Shape", parent=transform_node)
        else:
            overlay_node = "R8HUD_Shape"
        self.show_hud(1, origin)
        self.Overlay_Default(origin)

    def SM_Open(self, origin):
        if self.core.appPlugin.pluginName == "Maya":
            pass
            
            
    def SM_Close(self, origin):
        if self.core.appPlugin.pluginName == "Maya":
            if self.cmds.objExists("R8HUD"):
                self.show_hud(0, origin)

                
    def SM_preBlast(self, origin):
        if self.core.appPlugin.pluginName == "Maya":
            self.apply_hud_settings(origin)

        
    def SM_Startup(self, origin):
        if self.core.appPlugin.pluginName == "Maya":
            if origin.className == "Playblast":

                self.hud_groupbox = QGroupBox("HUD")  # Создаем QGroupBox
                self.hud_layout = QVBoxLayout(self.hud_groupbox)  # Лэйаут для QGroupBox
                self.hud_groupbox.setLayout(self.hud_layout)  # Устанавливаем лэйаут

                self.w_hud = QWidget()
                self.lo_hud = QVBoxLayout()  # Меняем на QVBoxLayout
                self.lo_hud.setContentsMargins(9, 0, 9, 0)
                self.w_hud.setLayout(self.lo_hud)


                self.hud_checkboxes = {}  # Словарь для хранения чекбоксов
                
                for label_text, checked in self.hud_items:
                    h_layout = QHBoxLayout()  # Горизонтальный лэйаут для пары
                    label = QLabel(label_text)
                    checkbox = QCheckBox()
                    checkbox.setChecked(checked)
                    self.hud_checkboxes[label_text] = checkbox  # Сохраняем чекбокс
                    
                    h_layout.addWidget(label)
                    h_layout.addStretch()  # Растяжка
                    h_layout.addWidget(checkbox)
                    
                    self.lo_hud.addLayout(h_layout)  # Добавляем горизонтальный лэйаут в основной

                self.hud_layout.addWidget(self.w_hud)
                
                # Добавляем кнопку
                self.hud_button = QPushButton("preview HUD")
                #self.hud_button.clicked.connect(self.apply_hud_settings)  # Подключаем действие
                self.hud_button.clicked.connect(lambda: self.apply_hud_settings(origin))
                
                self.hud_layout.addWidget(self.hud_button)
                
                origin.verticalLayout.addWidget(self.hud_groupbox)
            elif origin.className == "Export":
                pass

    def onStateManagerOpenMa(self, *args):
        state_manager = args[0]
        base_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
        
        extra_path = os.path.join(base_dir, "maya", "StateManagerNodes", "StateUserInterfaces")
        if os.path.exists(extra_path):
            sys.path.append(extra_path)
        extra_path = os.path.join(base_dir, "maya", "StateManagerNodes")
        

        if os.path.exists(extra_path):
            sys.path.append(extra_path)

            for root, _, files in os.walk(extra_path):
                for file in files:
                    if file.endswith(".py") and not file.endswith("_ui.py"):
                        state_manager.loadStateTypeFromFile(os.path.join(root, file))
                        
                break 



    def apply_hud_settings(self, origin):
        

        
        self.load_Overlay(origin)
        settings = {label: checkbox.isChecked() for label, checkbox in self.hud_checkboxes.items()}


        #current_file = self.cmds.file(q=True, sn=True)
        #file_name = os.path.basename(current_file)
        #if "." in file_name:
            #file_name = file_name.split(".")[0]
            
        data = self.core.getScenefileData(self.cmds.file(q=1, sn=1))
        
        #keys = ['episode', 'sequence', 'shot', 'task', 'version']
        keys = ['episode', 'sequence', 'shot']
        if all(k in data for k in keys):
            shot_name = '_'.join(data[k] for k in keys)
        
        self.cmds.setAttr(f"{self.transform_node}.Comment", origin.stateManager.publishComment, type="string")
        self.cmds.setAttr(f"{self.transform_node}.Status", origin.l_taskName.text(), type="string")
        self.cmds.setAttr(f"{self.transform_node}.Scene", shot_name, type="string")

        
        self.cmds.setAttr(f"{self.transform_node}._Logo", settings.get("Logo:"))
        self.cmds.setAttr(f"{self.transform_node}._ShotName", settings.get("Shot Name:"))
        self.cmds.setAttr(f"{self.transform_node}._Comment", settings.get("Comment:"))
        self.cmds.setAttr(f"{self.transform_node}._Frame", settings.get("Frame:"))
        self.cmds.setAttr(f"{self.transform_node}._TimeCode", settings.get("Time Code:"))
        self.cmds.setAttr(f"{self.transform_node}._Camera", settings.get("Camera:"))
        
        


    def show_hud(self, state, origin):
        if state == 1:
            
            
            self.cmds.setAttr(f"{self.transform_node}._Logo", state)
            self.cmds.setAttr(f"{self.transform_node}._ShotName", state)
            self.cmds.setAttr(f"{self.transform_node}._Comment", state)
            self.cmds.setAttr(f"{self.transform_node}._Frame", state)
            self.cmds.setAttr(f"{self.transform_node}._TimeCode", state)
            self.cmds.setAttr(f"{self.transform_node}._Camera", state)

            cameras = self.cmds.ls(type='camera')
            current_camera= "none"
            focal_length = "none"
            for camera in cameras:
                transform_node = self.cmds.listRelatives(camera, parent=True)[0]
                is_renderable = self.cmds.getAttr(f"{camera}.renderable")
                if is_renderable == 1:
                    current_camera = transform_node

                    self.cmds.setAttr(f"{current_camera}.displaySafeAction", state)


            options = {
                "playblastOverrideViewport": True,
                "playblastShowCVs": False,
                "playblastShowCameras": False,
                "playblastShowClipGhosts": False,
                "playblastShowControllers": False,
                "playblastShowDeformers": False,
                "playblastShowDimensions": False,
                "playblastShowDynamicConstraints": False,
                "playblastShowDynamics": False,
                "playblastShowFluids": False,
                "playblastShowFollicles": False,
                "playblastShowGreasePencil": False,
                "playblastShowGrid": False,
                "playblastShowHUD": True,
                "playblastShowHairSystems": False,
                "playblastShowHandles": False,
                "playblastShowHoldOuts": False,
                "playblastShowHulls": False,
                "playblastShowIKHandles": False,
                "playblastShowImagePlane": True,
                "playblastShowJoints": False,
                "playblastShowLights": False,
                "playblastShowLocators": True,
                "playblastShowMotionTrails": False,
                "playblastShowNCloths": False,
                "playblastShowNParticles": False,
                "playblastShowNRigids": False,
                "playblastShowNURBSCurves": False,
                "playblastShowNURBSSurfaces": False,
                "playblastShowOrnaments": False,
                "playblastShowParticleInstancers": False,
                "playblastShowPivots": False,
                "playblastShowPlanes": False,
                "playblastShowPluginShapes": False,
                "playblastShowPolyMeshes": True,
                "playblastShowSelectionHighlighting": False,
                "playblastShowStrokes": False,
                "playblastShowSubdivSurfaces": False,
                "playblastShowTextures": True,
            }
            for key, value in options.items():
                self.cmds.optionVar(intValue=(key, int(value)))

            self.mel.eval("rebuildShowMenu;")
        else:
            
            if self.cmds.objExists('R8HUD'):
                self.cmds.delete('R8HUD')
        
    def Overlay_Default(self, origin):


        self.cmds.setAttr(f"{self.transform_node}.Text_padding", 10, type="string")
        self.cmds.setAttr(f"{self.transform_node}.FrameOffset", 1001, type="string")
        
        if not origin.curCam:
            cameras = self.cmds.ls(type='camera')
            current_camera= "none"
            focal_length = "none"
            for camera in cameras:
                transform_node = self.cmds.listRelatives(camera, parent=True)[0]
                is_renderable = self.cmds.getAttr(f"{camera}.renderable")
                if is_renderable == 1:
                    cam = transform_node
        else:
            cam = origin.curCam
        self.cmds.setAttr(f"{self.transform_node}.Camera", cam, type="string")

        
    def sm_export_exportAppObjects(
        self,
        origin,
        startFrame,
        endFrame,
        outputName,
        nodes=None,
        expType=None,
    ):
        self.cmds.select(clear=True)
        if nodes is None:
            maya = self.core.getPlugin("Maya")
            setName = maya.getSetPrefix() + maya.validate(origin.getTaskname())
            if not maya.isNodeValid(origin, setName):
                return 'Canceled: The selection set "%s" is invalid.' % setName

            self.cmds.select(self.cmds.listConnections(setName), noExpand=True)
            expNodes = origin.nodes
        else:
            self.cmds.select(nodes)
            expNodes = [
                x for x in nodes if "dagNode" in self.cmds.nodeType(x, inherited=True)
            ]

        if expType is None:
            expType = origin.getOutputType()



        if expType in [".usd", ".usda"]:
            self.cmds.select(expNodes)

            # Явный путь с нужным расширением
            outputPath = os.path.splitext(outputName)[0] + expType
            usd_format = "usda" if expType == ".usda" else "usd"
            selection = not origin.chb_wholeScene.isChecked()

            # Получаем кадры анимации
            #start_frame = int(self.cmds.playbackOptions(q=True, min=True))
            #end_frame = int(self.cmds.playbackOptions(q=True, max=True))

        #startFrame,
        #endFrame,

            # Удаляем файл, если существует
            if os.path.exists(outputPath):
                os.remove(outputPath)

            # Экспорт через mayaUSDExport
            self.cmds.mayaUSDExport(
                f=outputPath,
                selection=selection,
                mergeTransformAndShape=True,
                exportSkels="auto",
                exportSkin="auto",
                exportInstances=True,
                exportVisibility=True,
                stripNamespaces=False,
                exportUVs=True,
                exportColorSets=True,
                exportDisplayColor=True,
                shadingMode="useRegistry",
                materialsScopeName="Looks",
                frameRange=(startFrame, endFrame),
                defaultUSDFormat=usd_format
            )

        else:
            outputName = ""
        return outputName

        



