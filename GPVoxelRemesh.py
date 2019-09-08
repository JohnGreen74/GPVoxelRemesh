bl_info = {
    "name": "GP_CNV",
    "author": "Asch",
    "version": (1.1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object > GP_CNV_action",
    "description": "GreasePensil to VoxelMesh",
    "warning": "",
    "wiki_url": "",
    "category": "A_GPVoxelRemesh", #category in add-ons, preferences
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector

#TODO: check if bezier curve has a line

#real actions
def gpconvertor(self, context):
    
    #WORK with Grease Pencil object GPencil:
    bpy.ops.object.mode_set(mode='OBJECT')                                      #force switch to object mode
    bpy.ops.object.select_all(action='DESELECT')                                #deselect all # make sure we have GPencil selected 
    bpy.data.objects['GPencil'].select_set(True)  
    OB = bpy.data.objects.get("GPencil")
    bpy.context.view_layer.objects.active = OB
    
    
    bpy.ops.object.gpencil_modifier_apply(apply_as='DATA', modifier="Mirror")   #apply mirror modifier to grease pencil if exist 
    
    bpy.ops.gpencil.convert(type='CURVE', use_timing_data=True)                 #convert current stroke to curve
    
    #WORK with Curve object GP_Layer:
    bpy.ops.object.select_all(action='DESELECT')                                #deselect all
    bpy.data.objects['GP_Layer'].select_set(True)                               #select new GP_Layer only
    OB = bpy.data.objects['GP_Layer']                                           #assign GP_Layer to OB
    bpy.context.view_layer.objects.active = OB                                  #set GP_Layer active
    
    
    
    #if self.merge == True:
    #    OB_Old = OB
    bpy.data.objects['GP_Layer'].select_set(True)
    OB.name = "NewVoxelMesh"
    
    
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['GPencil'].select_set(True)            #delete GreasePencil object
    OB_X = bpy.data.objects['GPencil']                      #delete GreasePencil object
    bpy.context.view_layer.objects.active = OB_X            #delete GreasePencil object
    bpy.ops.object.delete()                                 #delete GreasePencil object
    
    #WORK with Curve object as with mesh:
    bpy.data.objects['NewVoxelMesh'].select_set(True)
    OB = bpy.data.objects['NewVoxelMesh']
    bpy.context.view_layer.objects.active = OB
    

    bpy.context.object.data.bevel_depth = self.bevel_depth/200
    bpy.context.object.data.resolution_u = 1
    bpy.context.object.data.bevel_resolution = self.bevel_resolution;

    
    bpy.ops.object.convert(target='MESH')
    
    #WORK with mesh object:
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_mode(type="EDGE")
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.mesh.fill_holes(sides=0)
    bpy.ops.object.editmode_toggle()
    bpy.context.object.data.remesh_voxel_size = self.remesh_voxel_size / 100
    bpy.context.object.data.remesh_smooth_normals = self.smooth
    
    if self.xmirror == True:
        bpy.ops.object.modifier_add(type='MIRROR')
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Mirror")


    if self.merge == False:
        bpy.ops.object.voxel_remesh()
    
    if self.merge == True:
        OB = None
        OB = bpy.data.objects.get("VoxelMesh")
        if OB is None:
            OB = bpy.data.objects['NewVoxelMesh']
            bpy.data.objects['NewVoxelMesh'].select_set(True)
            OB.name = "VoxelMesh" 
            bpy.ops.object.voxel_remesh()
        else:
            bpy.data.objects['VoxelMesh'].select_set(True)          #select and set active old VoxelMesh to preserve all modifiers there
            bpy.context.view_layer.objects.active = OB              #set active
            bpy.ops.object.join()
            bpy.context.object.data.remesh_voxel_size = self.remesh_voxel_size / 100
            bpy.context.object.data.remesh_smooth_normals = self.smooth
            bpy.ops.object.voxel_remesh()      
    elif self.join == True:
        OB = None
        OB = bpy.data.objects.get("VoxelMesh")
        if OB is None:
            OB = bpy.data.objects['NewVoxelMesh']
            bpy.data.objects['NewVoxelMesh'].select_set(True)
            OB.name = "VoxelMesh" 
        else:
            bpy.data.objects['VoxelMesh'].select_set(True)          #select and set active old VoxelMesh to preserve all modifiers there
            bpy.context.view_layer.objects.active = OB              #set active
            bpy.ops.object.join()
            bpy.context.object.data.remesh_smooth_normals = self.smooth   
    else:  
        OB = bpy.data.objects['NewVoxelMesh']
        bpy.data.objects['NewVoxelMesh'].select_set(True)
        OB.name = "VoxelMesh" 
        
    bpy.ops.object.mode_set(mode='SCULPT')  



def gpfastcreate(self, context):
    
    if self.join == True:
        bpy.ops.object.mode_set(mode='OBJECT')                                      #force switch to object mode
        OB = bpy.context.view_layer.objects.active
        OB.name = "VoxelMesh" 
    
    
    bpy.ops.object.gpencil_add(location=(0, 0, 0), type='EMPTY')
    if self.xmirror == True:
        bpy.ops.object.gpencil_modifier_add(type='GP_MIRROR')
    bpy.ops.gpencil.paintmode_toggle()
    




class OBJECT_OT_Asch_gp_to_mesh(Operator):
    """Create a new Mesh Object"""
    bl_idname = "mesh.gpconvertor"  #id operator in keymap preferences
    bl_label = "GP to mesh convertor" #name in keymap preferences
    bl_options = {'REGISTER', 'UNDO'}
    
    #limit = bpy.props.FloatProperty(name="limit", default=0.1)
    bevel_depth = bpy.props.FloatProperty(name="bevel_depth*100", default=1)
    bevel_resolution = bpy.props.FloatProperty(name="bevel_resolution", default=0)
    #resolution_u = bpy.props.FloatProperty(name="resolution_u", default=1)
    remesh_voxel_size = bpy.props.FloatProperty(name="voxel_size*100", default=5, min=1, max=100)
    smooth = bpy.props.BoolProperty(name="smooth", default=False)
    merge = bpy.props.BoolProperty(name="remesh with previous", default=False)
    join = bpy.props.BoolProperty(name="join with previous", default=False)
    xmirror = bpy.props.BoolProperty(name="X Mirror", default=False)
    
    

    def execute(self, context):

        OB = None
        OB = bpy.data.objects.get("GPencil")
        if OB is None:  
            gpfastcreate(self, context)
        else:
            gpconvertor(self, context)

        return {'FINISHED'}


# Registration
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_Asch_gp_to_mesh.bl_idname,
        text="GP_CNV_action",
        icon='PLUGIN')



def register():
    bpy.utils.register_class(OBJECT_OT_Asch_gp_to_mesh)
    bpy.types.VIEW3D_MT_object.append(add_object_button)
    


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_Asch_gp_to_mesh)
    bpy.types.VIEW3D_MT_object.remove(add_object_button)


if __name__ == "__main__":
    register()
