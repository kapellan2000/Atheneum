import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.api.OpenMayaRender as omr
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds
from maya import mel

PLUGIN_NODE_NAME = "OverlayTextNode"
PLUGIN_NODE_ID = om.MTypeId(0x0011CF70)

def maya_useNewAPI():
    pass

class ShotMaskData(om.MUserData):
    """
    """

    def __init__(self):
        """
        """
        super(ShotMaskData, self).__init__(False)

        self.parsed_fields = []

        self.current_time = 0
        self.counter_padding = 4
        
        self.cam = ""

        self.font_color = om.MColor((1.0, 1.0, 1.0))
        self.font_scale = 1.0
        self.text_padding = 10

        self.top_border = True
        self.bottom_border = True
        self.border_color = om.MColor((0.0, 0.0, 0.0))

        self.vp_width = 0
        self.vp_height = 0

        self.mask_width = 0
        self.mask_height = 0

        self.drawContent = []
        
        self.sceninf = ""
        self.comm = ""



class OverlayTextNode(omui.MPxLocatorNode):
    def __init__(self):
        super(OverlayTextNode, self).__init__()

    def draw(self, view, path, style, status):
        pass  # Мы используем MPxDrawOverride для рендеринга

    @staticmethod
    def creator():
        return OverlayTextNode()

    @staticmethod
    def initialize():
        def create_string_attr(long_name, short_name):
            typed_attr_fn = om.MFnTypedAttribute()
            attr = typed_attr_fn.create(long_name, short_name, om.MFnData.kString)
            typed_attr_fn.writable = True
            typed_attr_fn.storable = True
            return attr
        
        OverlayTextNode.comment = create_string_attr("Comment", "cm")
        OverlayTextNode.addAttribute(OverlayTextNode.comment)
        
        OverlayTextNode.status = create_string_attr("Status", "st")
        OverlayTextNode.addAttribute(OverlayTextNode.status)
        
        OverlayTextNode.scene = create_string_attr("Scene", "sc")
        OverlayTextNode.addAttribute(OverlayTextNode.scene)

        OverlayTextNode.camera = create_string_attr("Camera", "cmr")
        OverlayTextNode.addAttribute(OverlayTextNode.camera)

        OverlayTextNode.tpadding = create_string_attr("Text_padding", "tp")
        OverlayTextNode.addAttribute(OverlayTextNode.tpadding)
        
        OverlayTextNode.foffset = create_string_attr("FrameOffset", "fo")
        OverlayTextNode.addAttribute(OverlayTextNode.foffset)

        
        
        
        # Создание и добавление атрибутов
        def create_bool_attr(long_name, short_name):
            attr_fn = om.MFnNumericAttribute()
            attr = attr_fn.create(long_name, short_name, om.MFnNumericData.kBoolean, True)
            attr_fn.writable = True
            attr_fn.storable = True
            return attr
        
        OverlayTextNode.logo = create_bool_attr("_Logo", "lgo")
        OverlayTextNode.addAttribute(OverlayTextNode.logo)
        
        OverlayTextNode.shotName = create_bool_attr("_ShotName", "shn")
        OverlayTextNode.addAttribute(OverlayTextNode.shotName)
        
        OverlayTextNode.comment = create_bool_attr("_Comment", "cmn")
        OverlayTextNode.addAttribute(OverlayTextNode.comment)
        
        OverlayTextNode.frame = create_bool_attr("_Frame", "frm")
        OverlayTextNode.addAttribute(OverlayTextNode.frame)
        
        OverlayTextNode.tCode = create_bool_attr("_TimeCode", "tcd")
        OverlayTextNode.addAttribute(OverlayTextNode.tCode)
        
        OverlayTextNode.cam = create_bool_attr("_Camera", "cam")
        OverlayTextNode.addAttribute(OverlayTextNode.cam)
                
        
        #self.postConstructor()



    def postConstructor(self):

        pass




class OverlayTextDrawOverride(omr.MPxDrawOverride):
    @staticmethod
    def creator(obj):
        return OverlayTextDrawOverride(obj)


    def __init__(self, obj):

        if not isinstance(obj, om.MObject):
            raise ValueError("Expected MObject, got {0}".format(type(obj)))
        super(OverlayTextDrawOverride, self).__init__(obj, OverlayTextDrawOverride.draw)
        
    def isAlwaysDirty(self):
        return True
        
    def supportedDrawAPIs(self):
        #return omr.MRenderer.kOpenGL | omr.MRenderer.kDirectX11
        return (omr.MRenderer.kAllDevices)
        
    #def isBounded(self, objPath, cameraPath):
        #return True

    #def boundingBox(self, objPath, cameraPath):
    #    corner1 = om.MPoint(-0.5, -0.5, -0.5)
    #    corner2 = om.MPoint(0.5, 0.5, 0.5)
    #    return om.MBoundingBox(corner1, corner2)

    #def boundingBox(self, objPath, cameraPath):
    #    corner1 = om.MPoint(-1000000, -1000000, -1000000)
    #    corner2 = om.MPoint(1000000, 1000000, 1000000)
    #    return om.MBoundingBox(corner1, corner2)
        


    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        print("999999999999999999")
        data = oldData
        if not isinstance(data, ShotMaskData):
            data = ShotMaskData()
            
            
        node_obj = objPath.node()
        dep_fn = om.MFnDependencyNode(node_obj)
        arr = ["Comment","Status","Scene","Camera","Text_padding", "FrameOffset"]

        dict={}
        for key in arr:
            status_plug = dep_fn.findPlug(key, False)
            status_value = status_plug.asString()
            dict[key] = status_value 

        arr2 = ["_Logo","_ShotName","_Comment","_Frame","_TimeCode","_Camera"]
        dict2 = {}
        
        for key in arr2:


            plug = dep_fn.findPlug(key, False)
            if plug:
                dict2[key] = plug.asBool()
            else:
                dict2[key] = None  
        

        data.drawContent = dict2

        

            
        dag_fn = om.MFnDagNode(objPath)    
            
        #data.current_time = int(cmds.currentTime(q=True))
        frame = int(cmds.currentTime(q=True))
        #fps = 24 
        time_unit = cmds.currentUnit(q=1, t=1)
        index = mel.eval(f'getIndexFromCurrentUnitCmdValue("{time_unit}")') - 1
        fps_name = mel.eval(f'getTimeUnitDisplayString({index});')
        fps = int(fps_name.split(' ')[0])
        
        

        
        value = dict.get("FrameOffset", "0")
        if value.isdigit(): 
            offset = int(value)
        else:
            offset = 1000   
            
            
        value = dict.get("Text_padding", "10")
        if value.isdigit(): 
            data.text_padding = int(value)
        else:
            data.text_padding = 10
        

        data.sceninf =  dict["Scene"] #+ " (" + dict["Status"] + ")"
        data.comm =  "Note: " +  dict["Comment"]


    
        # Вычисляем смещённый таймкод
        adjusted_frame = max(0, frame - offset)  # Не даём уйти в отрицательные значения
    
        hours = int(adjusted_frame // (fps * 3600))
        minutes = int((adjusted_frame % (fps * 3600)) // (fps * 60))
        seconds = int((adjusted_frame % (fps * 60)) // fps)
        frames = int(adjusted_frame % fps)
        
        timecode = "F: " + str( f"{frame:04}")
        data.current_frame = timecode
        timecode = str( f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}")
        data.current_time = timecode

        r = 1
        g = 1
        b = 1
        a = 1
        
        data.font_color = om.MColor((r, g, b, a))
        
        r = 1
        g = 1
        b = 1
        a = 0.1        
        data.border_color = om.MColor((r, g, b, a))


        # cameras = cmds.ls(type='camera')
        # current_camera= "none"
        # focal_length = "none"
        # for camera in cameras:
            # transform_node = cmds.listRelatives(camera, parent=True)[0]
            # is_renderable = cmds.getAttr(f"{camera}.renderable")
            # if is_renderable == 1:
                # current_camera = transform_node
                # focal_length = cmds.camera(transform_node, query=True, focalLength=True)
        current_camera = dict["Camera"]   
        shape_node = cmds.listRelatives(current_camera, shapes=True)[0]
        focal_length = cmds.camera(shape_node, query=True, focalLength=True)

        if current_camera.startswith("|"):
            #current_camera = current_camera[len("|"):]
            current_camera = current_camera.split("|")[-1]
        data.cam = (current_camera +" (F: "+str(round(focal_length))+")")
            
        
        
        vp_x, vp_y, data.vp_width, data.vp_height = frameContext.getViewportDimensions()
        if not (data.vp_width and data.vp_height):
            return None
            
        data.mask_width, data.mask_height = self.get_mask_width_height(cameraPath, data.vp_width, data.vp_height)
        if not (data.mask_width and data.mask_height):
            return None


        
        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        if not (data and isinstance(data, ShotMaskData)):
            return
            
            
        vp_half_width = 0.5 * data.vp_width
        vp_half_height = 0.5 * data.vp_height

        mask_half_width = 0.5 * data.mask_width
        mask_x = vp_half_width - mask_half_width
 
        mask_half_height = 0.5 * data.mask_height
        
        mask_bottom_y = vp_half_height - mask_half_height
        
        mask_top_y = vp_half_height + mask_half_height
        
        border_height = int(0.05 * data.mask_height * 1)

        drawManager.setColor(om.MColor((1.0, 1.0, 1.0, 1.0)))  # Белый цвет

        font_size = int(border_height - border_height * 0.25)#--------------------------------------------
        
        size_y = 50
        #font_size = 20
        background_size = (int(data.mask_width),size_y)


        #border
        #self.draw_border(drawManager, om.MPoint(mask_x, mask_top_y - size_y, 0.1), background_size, data.border_color)
        #self.draw_border(drawManager, om.MPoint(mask_x, mask_bottom_y, 0.1), background_size, data.border_color)
        
        #background_size = 15
        
        arr2 = ["_Logo","_ShotName","_Comment","_Frame","_TimeCode","_Camera"]
        if data.drawContent['_Logo']:
    
            path = "C:/ProgramData/Prism2/plugins/Atheneum/Scripts/maya/heroic_logo.png"
            texture_manager = omr.MRenderer.getTextureManager()
            texture = texture_manager.acquireTexture(path)
    
            drawManager.setTexture(texture)
            drawManager.setTextureSampler(omr.MSamplerState.kMinMagMipLinear, omr.MSamplerState.kTexClamp)
            drawManager.setTextureMask(omr.MBlendState.kRGBAChannels)
            drawManager.setColor(om.MColor((1.0, 1.0, 1.0, data.font_color.a)))
            
            
            # Scale the image based on the border height
            texture_desc = texture.textureDescription()
            scale_y = (0.5 * background_size[1]) - 4
            scale_x = scale_y / texture_desc.fHeight * texture_desc.fWidth

            
            
            position = om.MPoint(mask_x + data.text_padding, mask_top_y - border_height, 0.0)
            

            position = om.MPoint(position.x + scale_x, position.y + int( 0.4 *background_size[1])) #0.5 *
    
            drawManager.rect2d(position, om.MVector(0.0, 1.0, 0.0), scale_x, scale_y, True)



        #drawManager.setFontName("Orbitron")
        drawManager.setColor(data.font_color)
        drawManager.setFontSize(int(font_size*0.8))
        
        #drawManager.text2d(om.MPoint(mask_x + data.text_padding, mask_top_y - border_height, 0.0), status_value, omr.MUIDrawManager.kLeft, backgroundColor=om.MColor((0.0, 0.0, 0.0, 0.0)));
        if data.drawContent['_ShotName']:
            drawManager.text2d(om.MPoint(vp_half_width, mask_top_y - border_height, 0.0), data.sceninf, omr.MUIDrawManager.kCenter, backgroundColor=om.MColor((0.0, 0.0, 0.0, 0.0)));
            
        drawManager.setFontSize(int(font_size/2))
        if data.drawContent['_Comment']:   
            drawManager.text2d(om.MPoint(mask_x + data.mask_width - data.text_padding, mask_top_y - border_height, 0.0), data.comm, omr.MUIDrawManager.kRight, backgroundColor=om.MColor((0.0, 0.0, 0.0, 0.0)));
        #drawManager.setFontSize(font_size)
        if data.drawContent['_Frame']:   
            drawManager.text2d(om.MPoint(mask_x + data.text_padding, mask_bottom_y, 0),  data.current_frame , omr.MUIDrawManager.kLeft, backgroundColor=om.MColor((0.0, 0.0, 0.0, 0.0)));
            
        if data.drawContent['_TimeCode']:  
            drawManager.text2d(om.MPoint(vp_half_width, mask_bottom_y, 0.0),  data.current_time , omr.MUIDrawManager.kLeft, backgroundColor=om.MColor((0.0, 0.0, 0.0, 0.0)));
        
        if data.drawContent['_Camera']:  
            drawManager.text2d(om.MPoint(mask_x + data.mask_width - data.text_padding, mask_bottom_y, 0),data.cam, omr.MUIDrawManager.kRight, backgroundColor=om.MColor((0.0, 0.0, 0.0, 0.0)));

        
        drawManager.endDrawable()


    def get_mask_width_height(self, camera_path, vp_width, vp_height):
        camera_fn = om.MFnCamera(camera_path)


        camera_aspect_ratio = camera_fn.aspectRatio()
        device_aspect_ratio = cmds.getAttr("defaultResolution.deviceAspectRatio")

        vp_aspect_ratio = vp_width / float(vp_height)

        scale = 1.0


        mask_width = vp_width / camera_fn.overscan
        mask_height = mask_width / device_aspect_ratio
            
        return mask_width, mask_height
        
    def draw_border(self, draw_manager, position, background_size, color):
        """
        """
        draw_manager.text2d(position, " ", alignment=omr.MUIDrawManager.kLeft, backgroundSize=background_size, backgroundColor=color)



          
        
        
    def draw(context, data):
        """
        """
        print("drav----------")
        status = context.getDisplayStatus()

        if status == omr.MGeometryUtilities.displayStatusDormant:
            print("Объект в статусе kDormant")
        else:
            print(f"DisplayStatus: {status}")
        
        return

def initializePlugin(obj):
    plugin_fn = om.MFnPlugin(obj, "R8HUD", "1.0", "Any")  

    try:
        plugin_fn.registerNode(PLUGIN_NODE_NAME, PLUGIN_NODE_ID, OverlayTextNode.creator,
                               OverlayTextNode.initialize, ompx.MPxNode.kLocatorNode,
                               "drawdb/geometry/OverlayTextNode")
    except:
        om.MGlobal.displayError("Failed to register node: {0}".format(PLUGIN_NODE_NAME))

    try:
        # Теперь передаем правильный тип в MDrawRegistry
        omr.MDrawRegistry.registerDrawOverrideCreator("drawdb/geometry/OverlayTextNode",
                                                      "", OverlayTextDrawOverride.creator)
    except:
        om.MGlobal.displayError("Failed to register draw override: {0}".format(PLUGIN_NODE_NAME))

def uninitializePlugin(obj):
    plugin_fn = om.MFnPlugin(obj)

    try:
        omr.MDrawRegistry.deregisterDrawOverrideCreator("drawdb/geometry/OverlayTextNode", "")
        plugin_fn.deregisterNode(PLUGIN_NODE_ID)
    except:
        om.MGlobal.displayError("Failed to deregister plugin")
        raise