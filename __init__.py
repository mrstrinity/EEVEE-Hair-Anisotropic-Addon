bl_info = {
          "name": "EEVEE Anisotropy Hair Addon!",
          "author": "mrstrinity",
          "version": (1, 0),
          "blender": (3, 6, 15),
          "location": "Shader Editor > Shift+A",
          "category": "Node",
          "description": "Why doesn't Blender have anisotrophy for EEVE by default? No matter. Here it is."
}

# Refence the other codes python scripts, or it won't work.
from . import strands

# You need this too, or the code won't work at all.
import bpy
import os

# Submenu for the nodes. When you press Shift + A, you should see it.
class NODE_MT_hairpak(bpy.types.Menu):
          bl_label = "EEVEE Hair Anisotropy Pak"
          bl_idname = "NODE_MT_hairpak"
          
          def draw(self, context):
                    layout = self.layout
                    # This is where we start rferencing the nodes.
                    layout.operator("node.add_workaround", text="Hair Anisotropy", icon='NODETREE')
                    layout.operator("node.add_strands", text="Hair Strands", icon='NODETREE')

#Where the anisotropic node reference starts:
NODE_GROUP_NAME = "Hair anisotropy"

class NODE_OT_addworkaround(bpy.types.Operator):
          bl_idname = "node.add_workaround"
          bl_label = "Hair Anisotropy"
          bl_description = "Give your hair some shine!"
          bl_options = {'REGISTER', 'UNDO'}
          
          def execute(self, context):
                    # In node tree?
                    if context.space_data.tree_type != 'ShaderNodeTree':
                              self.report({'WARNING'}, "Not in Shader Editor")
                              return {'CANCELLED'}
                    
                    #If the node group isn't loaded in, append it there.
                    if NODE_GROUP_NAME not in bpy.data.node_groups:
                    
                              addon_dir = os.path.dirname(__file__)
                              blend_path = os.path.join(addon_dir, "aniso.blend")
                              
                              if not os.path.exists(blend_path):
                                        self.report({'ERROR'}, "aniso.blend not found")
                                        return {'CANCELLED'}
                    
                              with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                                        if NODE_GROUP_NAME in data_from.node_groups:
                                                  data_to.node_groups = [NODE_GROUP_NAME]
                                        else:
                                                  self.report({'ERROR'}, "Node group not found in aniso.blend")
                                                  return {'CANCELLED'}
                                        
                    # Adds the node to where the cursor is.
                    node = context.space_data.edit_tree.nodes.new("ShaderNodeGroup")
                    node.node_tree = bpy.data.node_groups[NODE_GROUP_NAME]
                    node.location = context.space_data.cursor_location
          
                    return {'FINISHED'}
          
# Add to Material menu
def menu_func(self, context):
          if context.space_data and context.space_data.tree_type == 'ShaderNodeTree':
                    self.layout.menu("NODE_MT_hairpak", icon='NODETREE')
                     
# When the addon is enabled?
def register():
          bpy.utils.register_class(NODE_MT_hairpak)
          bpy.utils.register_class(NODE_OT_addworkaround)
          bpy.types.NODE_MT_add.append(menu_func)
          strands.register()

# When the addon is disabled?
def unregister():
          strands.unregister()
          bpy.types.NODE_MT_add.remove(menu_func)
          bpy.utils.unregister_class(NODE_OT_addworkaround)
          bpy.utils.unregister_class(NODE_MT_hairpak)
          
if __name__ == "__main__":
          register()