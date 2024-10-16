# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#  Copyright 2024(C) Eraldo Sammuri
# ##### END GPL LICENSE BLOCK #####


bl_info = {
    "name": "LODs easy generator",
    "description": "Addon to easily generate LODs",
    "author": "erasam",
    "version": (1, 1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > LODs generator",
    "warning": "", # used for warning icon and text in addons panel
    "doc_url": "",
    "tracker_url": "",
    "support": "COMMUNITY",
    "category": "Development"
}

import bpy

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

from math import radians
from collections import defaultdict
import os
import fnmatch

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class LODsGenerator_PG_SceneProperties(PropertyGroup):

    SearchBy: EnumProperty(
        name="Search by:",
        description="Decimate Type",
        items=[ ('OP1', "Collections", ""),
                ('OP2', "Meshes", ""),
              ]
        )
        
    SearchFilter: EnumProperty(
        name="Search filter:",
        description="Search filter",
        items=[ ('OP1', "All", ""),
                ('OP2', "By Name", ""),
              ]
        )
 
    NameFilter: StringProperty(
        name="Name filter",
        description="Name filter",
        default="*",
        maxlen=1024,
        )

    ExcludeNameFilter: BoolProperty(
        name="Exclude Name filter",
        description="Exclude Name filter",
        default = False
        )
 
    EnableCollectionsByIteration: BoolProperty(
        name="Enable Collections By Iteration",
        description="Enable Collections By Iteration",
        default = False
        )
        
    SubdivModifiers: EnumProperty(
        name="Subdiv Modifiers",
        description="Subdiv Modifiers",
        items=[ ('OP1', "Leave", ""),
                ('OP2', "Reduce level", ""),
                ('OP3', "Delete", ""),
              ]
        )
 
    ApplyAllModifiers:  EnumProperty(
        name="Apply All Modifiers",
        description="Apply All Modifiers",
        items=[ ('OP1', "Never", ""),
                ('OP2', "Start of Iteration", ""),
                ('OP3', "End of Iteration", ""),
                ('OP4', "Both Start and End of Iteration", ""),
              ]
        )
 
    DeleteExistingDecimateModifiers: BoolProperty(
        name="Delete existing Decimate Modifiers",
        description="Delete existing Decimate Modifiers",
        default = False
        )
  
    LODsStart: IntProperty(
        name = "LODs Start",
        description="Integer property",
        default = 0,
        min = 0,
        max = 9
        )

    LODsEnd: IntProperty(
        name = "LODs End",
        description="Integer property",
        default = 0,
        min = 0,
        max = 9
        )

    DecimateType: EnumProperty(
        name="Decimate Type",
        description="Decimate Type",
        items=[ ('OP1', "Collapse", ""),
                ('OP2', "Un-ubdivide", ""),
                ('OP3', "Planar", ""),
              ]
        )

    CollapseRatio: FloatProperty(
        name = "Collapse Ratio",
        description = "Collapse Ratio",
        default = 0.01,
        min = 0.01,
        max = 1
        )

    CollapseTriangulate: BoolProperty(
        name="Collapse Triangulate",
        description="Collapse Triangulate",
        default = False
        )

    UnSubdivideIterations: IntProperty(
        name = "Un-Subdivide Iterations",
        description="Un-Subdivide Iterations",
        default = 1,
        min = 1,
        max = 32767
        )

    PlanarAngleLimit: FloatProperty(
        name = "Planar Angle Limit",
        description = "Planar Angle Limit",
        default = 0.01,
        min = 0.01,
        max = 180.00
        )

    PlanarDelimit: EnumProperty(
        name="Planar Delimit",
        description="Planar Delimit",
        items=[ ('OP1', "Normal", ""),
                ('OP2', "Material", ""),
                ('OP3', "Seam", ""),
                ('OP4', "Sharp", ""),
                ('OP5', "UVs", ""),
              ]
        )
        
    AllBoundaries: BoolProperty(
        name="All Boundaries",
        description="All Boundaries",
        default = False
        )

    ApplyIncrementally: EnumProperty(
        name="Apply Incrementally",
        description="Apply Incrementally Decimate Parameters",
        items=[ ('OP1', "Never", ""),
                ('OP2', "Once", ""),
                ('OP3', "From LOD00 onwards", ""),
                ('OP4', "From LOD01 onwards", ""),
              ]
        )

    ExportPath: StringProperty(
        name = "Directory",
        description="Choose a Directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH' # FILE_PATH
        )
    
    ExportName: StringProperty(
        name="Filename",
        description="Export Filename",
        default="",
        maxlen=1024,
        )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------
##Enable Collections By Iteration
def enableCollectionsByIteration(context,iteration):
    print("Enable Collections By Iteration")
    #Retrieve all the collections belonging to Scene Collection (root)
    collectionList=context.view_layer.layer_collection.children 
    if collectionList:
        for col in collectionList:
            print("Collection:", col.name)
            if (fnmatch.fnmatch(col.name, "LOD0"+str(iteration))):
                #Unhide Collection in viewport
                print("Unhide Collection:", col.name)
                col.hide_viewport = False
                for obj in col.collection.all_objects:      #col.collection.all_objects selects Objects that are in this collection and its child collections
                    print("Object name:", obj.name)
                    if (obj.type == 'MESH'):
                        #Unhide collection Object in viewport
                        obj.hide_set(False)
            elif (fnmatch.fnmatch(col.name, "LOD0?")):
                #Hide Collection in viewport
                print("Hide Collection:", col.name)
                col.hide_viewport = True
                for obj in col.collection.all_objects:      #col.collection.all_objects selects Objects that are in this collection and its child collections
                    print("Object name:", obj.name)
                    if (obj.type == 'MESH'):
                        #Hide collection Object in viewport
                        obj.hide_set(True)

##Modify Subdiv modifiers
def modifySubdivModifiers(obj,operation):
    for m in obj.modifiers:
        if(m.type=="SUBSURF"):
            if operation == "OP2":
                #Reduce Subdiv level
                print("Decrease Subdiv modifier level")
                m.levels=m.levels-1
            elif operation == "OP3":
                #Remove Subdiv modifier
                print("Removing Subdiv modifier")
                obj.modifiers.remove(modifier=m)
               
##Cleans all decimate modifiers
def cleanAllDecimateModifiers(obj):
    for m in obj.modifiers:
        if(m.type=="DECIMATE"):
            print("Removing Decimate modifier")
            obj.modifiers.remove(modifier=m)

##Apply all modifiers
def applyAllModifiers(obj):
    ctx = bpy.context.copy()
    ctx['object'] = obj
    for _, m in enumerate(obj.modifiers):
        try:
            ctx['modifier'] = m
            bpy.ops.object.modifier_apply(ctx, modifier=m.name)
        except RuntimeError:
            print(f"Error applying {m.name} to {obj.name}, removing it instead.")
            obj.modifiers.remove(m)

    for m in obj.modifiers:
        obj.modifiers.remove(m)

def saveLODfile(exportPath,exportName,iteration):
    #Trim .blend estension
    indexOfText=exportName.rfind('.blend')
    if (indexOfText!=-1):
        exportName=exportName.split(".blend")[0]
 
    #Trim decimate version of file name
    indexOfText=exportName.rfind('_LOD')
    if(indexOfText!=-1):
        exportName=exportName.split("_LOD")[0]

    exportName='{}{}{}{}'.format(exportName, "_LOD0",str(iteration),".blend")
    print("Saving file:", exportPath+exportName)
    bpy.ops.wm.save_as_mainfile(filepath=exportPath+exportName)

    
class LODsGenerator_OT_generateLODs(Operator):
    """Generate LOD files"""
    bl_idname = "lodsgenerator.generatelods"
    bl_label = "Generate LOD files"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        scene = context.scene
        LODsGeneratortool = scene.LODsGenerator_tool
        object = context.object
        
        if LODsGeneratortool.DecimateType == "OP1":
            decimateType="COLLAPSE"
        elif LODsGeneratortool.DecimateType == "OP2":
            decimateType="UNSUBDIV"    #Un-Subdivide
        else:
            decimateType="DISSOLVE"    #Planar
            if LODsGeneratortool.PlanarDelimit == "OP1":
                planarDelimit={"NORMAL"}
            elif LODsGeneratortool.PlanarDelimit == "OP2":
                planarDelimit={"MATERIAL"}
            elif LODsGeneratortool.PlanarDelimit == "OP3":
                planarDelimit={"SEAM"}
            elif LODsGeneratortool.PlanarDelimit == "OP4":
                planarDelimit={"SHARP"}
            else:
                planarDelimit={"UV"}

        #Retrieve list of Mesh Objects matching selection parameters
        objectList = defaultdict(list)
        objectMeshList = defaultdict(list)
        if LODsGeneratortool.SearchBy == "OP1" and LODsGeneratortool.SearchFilter == "OP2" and LODsGeneratortool.NameFilter != "*":
            #By Collection and By Name -> not working with wildcard
            print("By Collection and By Name")
            col = bpy.data.collections.get(LODsGeneratortool.NameFilter)
            if col:
                objectList=col.objects      #col.all_objects selects Objects that are in this collection and its child collections
        elif LODsGeneratortool.SearchBy == "OP2" and LODsGeneratortool.SearchFilter == "OP2" and LODsGeneratortool.NameFilter != "*":
            #By Meshes and By Name
            print("By Mesh and By Name")
            objectList = [obj for obj in bpy.data.objects if fnmatch.fnmatch(obj.name, LODsGeneratortool.NameFilter)]
        else:
            print("All objects")
            objectList=bpy.data.objects
        if objectList:
            objectMeshList = set(o.data for o in objectList if o.type == 'MESH')   

        for iteration in range(LODsGeneratortool.LODsStart,LODsGeneratortool.LODsEnd+1):
            print("Iteration", iteration)
            if (LODsGeneratortool.EnableCollectionsByIteration):
                enableCollectionsByIteration(context, iteration)
 
            modifierName="LOD0"+str(iteration)

            for obj in objectList:
                if (obj.type == 'MESH') and (obj.hide_get() == False):
                    print("\tRetrieved mesh object:", obj.name)

                    if (LODsGeneratortool.SubdivModifiers != "OP1"):
                        modifySubdivModifiers(obj,LODsGeneratortool.SubdivModifiers)

                    if (LODsGeneratortool.DeleteExistingDecimateModifiers):
                        cleanAllDecimateModifiers(obj)

                    if (LODsGeneratortool.ApplyAllModifiers == "OP2" or LODsGeneratortool.ApplyAllModifiers == "OP4"):
                        applyAllModifiers(obj)

                    modifier=obj.modifiers.new(modifierName,'DECIMATE')
                    modifier.decimate_type=decimateType
                    
                    if (LODsGeneratortool.ApplyIncrementally == "OP1"):          #Never
                        increment=0
                    elif (LODsGeneratortool.ApplyIncrementally == "OP2"):        #Once
                        increment=1
                    elif (LODsGeneratortool.ApplyIncrementally == "OP3"):        #From LOD00 onwards
                        increment=iteration+1
                    else:                                                       #From LOD01 onwards
                        increment=iteration
                    
                    if decimateType == "COLLAPSE":
                        modifier.ratio=1-LODsGeneratortool.CollapseRatio*increment
                        modifier.use_collapse_triangulate=LODsGeneratortool.CollapseTriangulate
                    elif decimateType == "UNSUBDIV":
                        modifier.iterations=LODsGeneratortool.UnSubdivideIterations*increment
                    else:
                        modifier.angle_limit=radians(LODsGeneratortool.PlanarAngleLimit)*increment
                        modifier.delimit=planarDelimit
                        modifier.use_dissolve_boundaries=LODsGeneratortool.AllBoundaries

                    if (LODsGeneratortool.ApplyAllModifiers == "OP3" or LODsGeneratortool.ApplyAllModifiers == "OP4"):
                        applyAllModifiers(obj)

            if LODsGeneratortool.ExportName:
                saveLODfile(LODsGeneratortool.ExportPath,LODsGeneratortool.ExportName,iteration)

        return {'FINISHED'}
        
class WM_OT_PrintParams(Operator):
    bl_label = "Print parameter values to the Console"
    bl_idname = "wm.print_params" 
    # WindowManager namespace (wm.hello...) serves as example,
    # You could also use a custom one like: LODsGenerator_category.hello_world
    
    def execute(self, context):
        scene = context.scene
        LODsGeneratortool = scene.LODsGenerator_tool

        # print the values to the console
        print("LODS Easy Generator parameters:")

        print("Search By:", LODsGeneratortool.SearchBy)
        print("Search Filter:", LODsGeneratortool.SearchFilter)
        print("Name Filter:", LODsGeneratortool.NameFilter)
        print("Exclude Name Filter:", LODsGeneratortool.ExcludeNameFilter)

        print("LODS Start:", LODsGeneratortool.LODsStart)
        print("LODS End:", LODsGeneratortool.LODsEnd)
        
        print("Enable Collections by Iteration:", LODsGeneratortool.EnableCollectionsByIteration)     
        
        print("Modify Subdiv Modifiers:", LODsGeneratortool.SubdivModifiers)
        print("Delete Existing Decimate Modifiers:", LODsGeneratortool.DeleteExistingDecimateModifiers)
        print("Apply All Modifiers:", LODsGeneratortool.ApplyAllModifiers)

        print("Decimate Type:", LODsGeneratortool.DecimateType)
        
        print("Collapse Ratio:", LODsGeneratortool.CollapseRatio)
        print("Collapse Triangulate:", LODsGeneratortool.CollapseTriangulate)
        
        print("UnSubdivide Iterations:", LODsGeneratortool.UnSubdivideIterations)
        
        print("PlanarAngle Limit:", LODsGeneratortool.PlanarAngleLimit)
        print("Planar Delimit:", LODsGeneratortool.PlanarDelimit)
        print("All Boundaries:", LODsGeneratortool.AllBoundaries)

        print("Apply Incrementally:", LODsGeneratortool.ApplyIncrementally)

        filepath = bpy.data.filepath
        directory = os.path.dirname(filepath)
        print("File Path:", directory)
        print("Export Path:", LODsGeneratortool.ExportPath)
      
        print("File Name:", bpy.path.basename(bpy.context.blend_data.filepath))
        print("Export Name:", LODsGeneratortool.ExportName)
        
        return {'FINISHED'}
    
# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "LODs Easy Generator"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "LODs Easy Generator"
    bl_context = "objectmode"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        scene = context.scene
        LODsGeneratortool = scene.LODsGenerator_tool

        row = self.layout.row()
        row.label(text="____________________________________________________________________________________")
        row = self.layout.row()
        row.label(text="LODs generator parameters")

        layout.prop(LODsGeneratortool, "SearchBy", expand=True)
        layout.prop(LODsGeneratortool, "SearchFilter", expand=True)
        if LODsGeneratortool.SearchFilter=="OP2":
            #Enable NameFilter and ExcludeNameFilter if SearchFilter is Name   
            layout.prop(LODsGeneratortool, "NameFilter")
            #layout.prop(LODsGeneratortool, "ExcludeNameFilter")

        layout.prop(LODsGeneratortool, "LODsStart")
        layout.prop(LODsGeneratortool, "LODsEnd")
        
        layout.prop(LODsGeneratortool, "EnableCollectionsByIteration")  

        layout.prop(LODsGeneratortool, "SubdivModifiers")        
        layout.prop(LODsGeneratortool, "DeleteExistingDecimateModifiers")
        layout.prop(LODsGeneratortool, "ApplyAllModifiers")

        layout.prop(LODsGeneratortool, "DecimateType", expand=True)
 
        if LODsGeneratortool.DecimateType == "OP1":     #Collapse
            layout.prop(LODsGeneratortool, "CollapseRatio")
            layout.prop(LODsGeneratortool, "CollapseTriangulate")
        elif LODsGeneratortool.DecimateType == "OP2":   #Un-Subdivide
            layout.prop(LODsGeneratortool, "UnSubdivideIterations")
        else:                                           #Planar
            layout.prop(LODsGeneratortool, "PlanarAngleLimit")
            layout.prop(LODsGeneratortool, "PlanarDelimit")
            layout.prop(LODsGeneratortool, "AllBoundaries")

        layout.prop(LODsGeneratortool, "ApplyIncrementally")

        row = self.layout.row()
        row.label(text="____________________________________________________________________________________")
        row = self.layout.row()
        row.label(text="LODs export parameters")
        filepath = bpy.data.filepath
        directory = os.path.dirname(filepath)
        layout.prop(LODsGeneratortool, "ExportPath")     
        #LODsGeneratortool.ExportPath.default=directory
        layout.prop(LODsGeneratortool, "ExportName")
        #LODsGeneratortool.ExportName.default=bpy.path.basename(bpy.context.blend_data.filepath)     

        row = self.layout.row()
        row.label(text="____________________________________________________________________________________")
        layout.separator(factor=1.5)

        #layout.operator("wm.print_params")
        #layout.separator()

        layout.operator("lodsgenerator.generatelods")
        layout.separator()
 

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    WM_OT_PrintParams,
    LODsGenerator_OT_generateLODs,
    LODsGenerator_PG_SceneProperties,
    OBJECT_PT_CustomPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.LODsGenerator_tool = PointerProperty(type=LODsGenerator_PG_SceneProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.LODsGenerator_tool


if __name__ == "__main__":
    register()