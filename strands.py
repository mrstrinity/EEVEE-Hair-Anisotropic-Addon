import bpy
import os

# Hairstand node reference START!
NODE_GROUP_NAME = "HairStrands"

class NODE_OT_addstrands(bpy.types.Operator):
          bl_idname = "node.add_strands"
          bl_label = "Hair Strands"
          bl_description = "Hair strand details!"
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
          
# There's no need for a menu function. Otherwise, it'll just show up twice. 

def register():
          bpy.utils.register_class(NODE_OT_addstrands)
          
def unregister():
          bpy.utils.unregister_class(NODE_OT_addstrands)