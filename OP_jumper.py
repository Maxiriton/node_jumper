import bpy
from bpy.types import Operator, PropertyGroup
from bpy.props import (
                    FloatVectorProperty,
                    StringProperty,
                    IntProperty
                    )
from mathutils import Vector

def get_min_max_coordinates(context) ->tuple[float]:
    ''' Get the min max coordinates of given nodes.
        Returns : Xmin, Xmax, Ymin, Ymax'''
    return (0,0,0,0)

def get_int_from_enum(enum_string:str) -> int:
    if enum_string == 'ZER0':
        return 0
    elif enum_string == 'ONE':
        return 1 
    elif enum_string == 'TWO':
        return 2 
    elif enum_string == 'THREE':
        return 3 
    elif enum_string == 'FOUR':
        return 4 
    elif enum_string == 'FIVE':
        return 5 
    elif enum_string == 'SIX':
        return 6 
    elif enum_string == 'SEVEN':
        return 7 
    elif enum_string == 'EIGHT':
        return 8 
    elif enum_string == 'NINE':
        return 9 
    else: 
        return -1



class NodeJumpObject(PropertyGroup):
    center : FloatVectorProperty(default=(0,0,0))
    editor : StringProperty()
    dimensions : FloatVectorProperty()
    shortcut : IntProperty() #store the value from 0 to 9


    def setup(self, context, shortcut):
        tree_center = context.space_data.edit_tree.view_center
        self.center = (tree_center[0], tree_center[1], 0)
        self.shortcut = shortcut

def get_jump_object_by_shortcut(context, shortcut):
    for jumpObject in context.scene.NodeJumpObjects:
        if jumpObject.shortcut == shortcut:
            return jumpObject

    return None


class RecordPosition(Operator):
    """Jump To Recorded Position"""
    bl_idname = "jumper.record"
    bl_label = "Record New Position"
    bl_options = {'REGISTER','UNDO'}

    shortcut : IntProperty()

    def invoke(self, context, event):
        self.shortcut = get_int_from_enum(event.type)
        if self.shortcut == -1:
            return {'CANCELED'}
        print(self.shortcut)
        return self.execute(context)

    def execute(self, context):
        index_to_remove = -1
        for index, jumpObj in enumerate(context.scene.NodeJumpObjects):
            if jumpObj.shortcut == self.shortcut:
                index_to_remove = index

        if index_to_remove != -1:
            context.scene.NodeJumpObjects.remove(index_to_remove)
        
        jump_to_find = context.scene.NodeJumpObjects.add()
        jump_to_find.setup(context, self.shortcut)
        self.report({'INFO'}, f"Position stored at slot {self.shortcut}")
        return {'FINISHED'}


class JumpToPosition(Operator):
    """Jump To Recorded Position"""
    bl_idname = "jumper.jump"
    bl_label = "Jump to recorded position"
    bl_options = {'REGISTER','UNDO'}

    shortcut : IntProperty()

    def invoke(self, context, event):
        self.shortcut = get_int_from_enum(event.type)
        if self.shortcut == -1:
            return {'CANCELED'}
        print(self.shortcut)
        return self.execute(context)
    # @classmethod
    # def poll(cls, context):
    #     return context.mode == 'OBJECT'

    def execute(self, context):
        jump_object = get_jump_object_by_shortcut(context, self.shortcut)

        if not jump_object: 
            self.report({'INFO'}, f"No position stored for this slot!")
            return {'CANCELLED'}


        tree_center = context.space_data.edit_tree.view_center
        current_center_position = Vector((tree_center[0], tree_center[1], 0))
        delta  = Vector(jump_object.center) - current_center_position

        # print(f"La recorded position est {Vector(jump_object.center)}")
        # print(f"La current position est {current_center_position}")

        # print(delta)
        bpy.ops.view2d.pan(deltax=int(delta[0]) +1 , deltay=int(delta[1])+1)
        return {'FINISHED'}

### Registration

classes = (
    JumpToPosition,
    RecordPosition,
    NodeJumpObject
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.NodeJumpObjects = bpy.props.CollectionProperty(type = NodeJumpObject)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.NodeJumpObjects
