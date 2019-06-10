bl_info = {
    "name": "GP_CNV",
    "author": "Asch",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "A_GPVoxelRemesh", #category in add-ons, preferences
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

#real actions
def gpconvertor(self, context):
    bpy.ops.object.mode_set(mode='OBJECT')  
    bpy.ops.gpencil.convert(type='CURVE', use_timing_data=True)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['GP_Layer'].select_set(True)
    OB = bpy.data.objects['GP_Layer']
    bpy.context.view_layer.objects.active = OB
    
    if self.merge == True:
        OB_Old = OB
    bpy.data.objects['GP_Layer'].select_set(True)
    OB.name = "NewVoxelMesh"
    
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['GPencil'].select_set(True)
    OB_X = bpy.data.objects['GPencil']
    bpy.context.view_layer.objects.active = OB_X
    bpy.ops.object.delete()
    
    
    bpy.data.objects['NewVoxelMesh'].select_set(True)
    OB = bpy.data.objects['NewVoxelMesh']
    bpy.context.view_layer.objects.active = OB
    

    bpy.context.object.data.bevel_depth = self.bevel_depth/100
    bpy.context.object.data.resolution_u = 1


    bpy.ops.object.convert(target='MESH')
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.mesh.fill_holes(sides=0)
    bpy.ops.object.editmode_toggle()
    bpy.context.object.data.voxel_size = self.voxel_size / 100
    bpy.context.object.data.smooth_normals = self.smooth
    if self.merge == False:
        bpy.ops.object.remesh()
    
    if self.merge == True:
        OB = bpy.data.objects['VoxelMesh']
        bpy.data.objects['VoxelMesh'].select_set(True)
        bpy.ops.object.join()
        bpy.ops.object.remesh()
        #del OB_Old
    
    OB = bpy.data.objects['NewVoxelMesh']
    bpy.data.objects['NewVoxelMesh'].select_set(True)
    OB.name = "VoxelMesh"
    
    

def gpfastcreate(self, context):
    bpy.ops.object.mode_set(mode='OBJECT')  
    bpy.ops.object.gpencil_add(location=(0, 0, 0), type='EMPTY')
    bpy.ops.gpencil.paintmode_toggle()





class OBJECT_OT_Asch_gp_to_mesh(Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.gpconvertor"  #id operator in keymap preferences
    bl_label = "GP to mesh convertor" #name in keymap preferences
    bl_options = {'REGISTER', 'UNDO'}
    
    #limit = bpy.props.FloatProperty(name="limit", default=0.1)
    bevel_depth = bpy.props.FloatProperty(name="bevel_depth*100", default=1)
    voxel_size = bpy.props.FloatProperty(name="voxel_size*100", default=20, min=1, max=100)
    smooth = bpy.props.BoolProperty(name="smooth", default=False)
    merge = bpy.props.BoolProperty(name="merge with previous", default=True)
    

    def execute(self, context):

        gpconvertor(self, context)

        return {'FINISHED'}


class OBJECT_OT_Asch_new_gp(Operator):
    """Create a new GP Object"""
    bl_idname = "mesh.gpfastcreate"  #id operator in keymap preferences
    bl_label = "GP fast create" #name in keymap preferences
    bl_options = {'REGISTER', 'UNDO'}
    
    #limit = bpy.props.FloatProperty(name="limit", default=0.1)
    #bevel_depth = bpy.props.FloatProperty(name="bevel_depth*100", default=1)
    #voxel_size = bpy.props.FloatProperty(name="voxel_size*100", default=20, min=1, max=100)
    #smooth = bpy.props.BoolProperty(name="smooth", default=False)
    

    def execute(self, context):

        gpfastcreate(self, context)

        return {'FINISHED'}

# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_Asch_gp_to_mesh.bl_idname,
        text="GP_CNV_action1",
        icon='PLUGIN')

def add_object_button2(self, context):
    self.layout.operator(
        OBJECT_OT_Asch_new_gp.bl_idname,
        text="GP_CNV_action2",
        icon='PLUGIN')


def register():
    bpy.utils.register_class(OBJECT_OT_Asch_gp_to_mesh)
    bpy.types.VIEW3D_MT_object.append(add_object_button)
    bpy.utils.register_class(OBJECT_OT_Asch_new_gp)
    bpy.types.VIEW3D_MT_object.append(add_object_button2)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Asch_gp_to_mesh)
    bpy.types.VIEW3D_MT_object.remove(add_object_button)


if __name__ == "__main__":
    register()
