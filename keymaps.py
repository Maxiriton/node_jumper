'''Global KeyMap managment'''

import bpy
import bpy
import time
import numpy as np
from bpy.types import Operator
from bpy.props import BoolProperty
addon_keymaps = []

def register_keymaps():
    addon = bpy.context.window_manager.keyconfigs.addon

    ## Sculpt mode toggles
    km = addon.keymaps.new(name = "Screen Editing", space_type = "EMPTY", region_type='WINDOW')

    kmi = km.keymap_items.new('jumper.record', type='ONE', value='PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new('jumper.record', type='TWO', value='PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new('jumper.record', type='THREE', value='PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new('jumper.jump', type='ONE', value='PRESS')
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new('jumper.jump', type='TWO', value='PRESS')
    addon_keymaps.append((km, kmi))

    kmi = km.keymap_items.new('jumper.jump', type='THREE', value='PRESS')
    addon_keymaps.append((km, kmi))


def unregister_keymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
   
    addon_keymaps.clear()
def register():
    if not bpy.app.background:
        register_keymaps()

def unregister():
    if not bpy.app.background:
        unregister_keymaps()

if __name__ == "__main__":
    register()