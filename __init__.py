# -*- coding: utf-8 -*-
bl_info = {
    "name": "Modify Image Alpha",
    "author": "Demingo Hill (Noizirom)",
    "version": (0, 1),
    "blender": (4, 2, 1),
    "location": "View3D > Sidebar > Modify Image Alpha",
    "description": "An addon to modify the alpha values of an image based on values from an image mask.",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
}

u"\\u00A9" "Demingo Hill"

import bpy
from bpy.types import Panel, Operator, PropertyGroup, Scene
from bpy.props import PointerProperty, StringProperty, BoolProperty
from bpy.utils import register_class, unregister_class
from pathlib import Path
from numpy import array




def get_pixels(img):
    data = array(img.pixels)
    return data.reshape((int(data.size//4), 4))


def set_diffuse_alpha(diffuse, alpha, copy_alpha=False):
    dp = get_pixels(diffuse)
    ap = get_pixels(alpha)
    if copy_alpha:
        dp[:,3] = ap[:,3]
    else:
        dp[:,3] = ap[:,0]
    diffuse.pixels = dp.ravel()
    diffuse.pixels.update()


def validate_files(src, alpha):
    sf = Path(src)
    af = Path(alpha)
    return (str(sf.suffix) == '.png') and (str(af.suffix) == '.png')


def modify_image_alpha(self, context):
    scene = context.scene
    mod_props = scene.mod_img_alpha_props
    diffuse = bpy.data.images.load(filepath=str(mod_props.src_file))
    alpha = bpy.data.images.load(filepath=str(mod_props.alpha_file))
    set_diffuse_alpha(diffuse, alpha, copy_alpha=mod_props.copy_alpha)
    diffuse.save_render(filepath=str(mod_props.src_file))
    bpy.data.images.remove(diffuse)
    bpy.data.images.remove(alpha)


def modify_image_alpha_draw(self, context):
    layout_dock = self.layout
    scene = context.scene
    mod_props = scene.mod_img_alpha_props
    mbox = layout_dock.box()
    col = mbox.column()
    col.prop(mod_props, "src_file", text="Source Image")
    col.separator()
    col.prop(mod_props, "alpha_file", text="Alpha Image")
    col.separator()
    op_col = col.row()
    op_col.operator("image.modify_image_alpha", text="Modify")
    op_col.prop(mod_props, "copy_alpha", text="")


class ModifyImageAlphaProps(PropertyGroup):
    """
    """
    src_file: StringProperty(name="Source File", description="Source image for alpha modification.", default="", subtype="FILE_PATH")
    
    alpha_file: StringProperty(name="Alpha File", description="Alpha image used to modify source image.", default="", subtype="FILE_PATH")
    
    copy_alpha: BoolProperty(name="Copy Alpha", description="Copy the alpha of the alpha image to the source image.", default=False)
 

class MODIFYALPHATEXTURE_PT_layout_panel(Panel):
    bl_label = "Modify Image Alpha"
    bl_category = "Modify Image Alpha"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        modify_image_alpha_draw(self, context)
 

class ModifyImageAlphaOp(Operator):
    """
    """
    bl_idname = "image.modify_image_alpha"
    bl_label = "Modify Image Alpha"
    bl_description = "Modify the alpha of a source image by using data from another image."
    
    @classmethod
    def poll(cls, context):
        scene = context.scene
        mod_props = scene.mod_img_alpha_props
        src_file = mod_props.src_file
        alpha_file = mod_props.alpha_file
        return validate_files(src_file, alpha_file)
    
    def execute(self, context):
        modify_image_alpha(self, context)
        return {'FINISHED'}

 
 
 
classes = [
    ModifyImageAlphaProps,
    ModifyImageAlphaOp,
    MODIFYALPHATEXTURE_PT_layout_panel,
 ]
 
 
 
def register():
    for cls in classes:
        register_class(cls)
    
    Scene.mod_img_alpha_props = PointerProperty(type=ModifyImageAlphaProps)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
    
    del Scene.mod_img_alpha_props
 

if __name__ == "__main__":
    register()








