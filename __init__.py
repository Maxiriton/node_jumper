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
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Node Jumper",
    "author": "Henri Hebeisen",
    "version": (0, 0, 1),
    "blender": (3, 4, 1),
    "location": "Node Editors",
    "description": "Immediate save and load view position to quickly navigate position",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
    }

import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, EnumProperty, FloatProperty, StringProperty
from . import OP_jumper

class JP_prefs(AddonPreferences):
    bl_idname = __package__

        ## tabs
    
    pref_tabs : EnumProperty(
        items=(('PREF', "Preferences", "Change some preferences of the modal"),
               ('KEYS', "Shortcuts", "Customize addon shortcuts")
               ),
               default='PREF')

    is_locked_by_default : BoolProperty(
        name="Lock 3D View By Default",
        default=True
    )

    interpolator_sensitivity : FloatProperty(
        name="Intepolator Sensivity",
        default = 0.5,
        soft_min=0.01,
        soft_max=1
    )

    grease_pencil_default_object : StringProperty(
        name="Grease Pencil Object",
        description="Default Grease Pencil Object name. Will be used for TVPaint Importer as default object to import keys into",
        default="Trait"
    )

    export_folder_default : StringProperty(
        name="Default Exports folder",
        description="Folder name for exports, should be relative to work correctly",
        default="//../EXPORTS/",
        subtype='DIR_PATH'
    )

    def draw(self, context):
        layout = self.layout

        row= layout.row(align=True)
        row.prop(self, "pref_tabs", expand=True)

        if self.pref_tabs == 'PREF':
            box = layout.box()
            box.label(text='Project settings')
            box.prop(self, "is_locked_by_default")

            box.prop(self, "interpolator_sensitivity")
            box.prop(self, "grease_pencil_default_object")
            box.prop(self, "export_folder_default")
            
        if self.pref_tabs == 'KEYS':
            box = layout.box()
            box.label(text='Shortcuts added by 3.0 Tools with context scope:')

            prev_key_category = ''
            for kms in [
                        UI_gp_draw_keymap.addon_keymaps,
                        UI_gp_edit_keymap.addon_keymaps,
                        UI_gp_sculpt_keymap.addon_keymaps,
                        UI_gp_edit_pie_menu.addon_keymaps,
                        ]:

                for akm, akmi in kms:
                    km = context.window_manager.keyconfigs.user.keymaps.get(akm.name)
                    if not km:
                        continue
                    key_category = km.name
                    # kmi = km.keymap_items.get(akmi.idname) # get only first idname when multiple entry
                    kmi = None

                    ## numbering hack, need a better way to find multi idname user keymaps
                    for km_item in km.keymap_items:
                        if km_item.idname == akmi.idname:
                            kmi = km_item
                            break

                    if not kmi:
                        continue
                
                    ## show keymap category (ideally grouped by category)
                    if not prev_key_category:
                        if key_category:
                            box.label(text=key_category)
                    elif key_category and key_category != prev_key_category: # check if has changed singe
                        box.label(text=key_category)

                    draw_kmi(km, kmi, box)
                    prev_key_category = key_category

                box.separator()







classes = (
    JP_prefs,
)

addon_modules = (
    OP_jumper,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    for mod in addon_modules:
        mod.register()

    # bpy.types.Scene.jumper_props = bpy.props.PointerProperty(type = Jumper_NodesSettings)


def unregister():
    for mod in reversed(addon_modules):
        mod.unregister()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # del bpy.types.Scene.gp_30_studio_props


if __name__ == "__main__":
    register()

