import bpy


#                              [ Written for Blender 4.1, using NinjaRipper 2.8 ]

# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 
#                                                                                                                     #
#       >>>>>>>>>>>>  CHANGE RENDER SAMPLING TO 512! THIS WILL OFFSET HOW NOISY THE EDGES ARE!  <<<<<<<<<<<<          #
#                                                                                                                     #
#     [[[[[ THIS SCRIPT *ADDITIONALLY* MAKES TEXTURES PIXELATED, MERGES VERTEXES, AND TUNES SHADERS VALUES! ]]]]]     #
#                                                                                                                     #
# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 

#                            /// RUNNING THIS SCRIPT ASSUMES YOU HAVE READ READ.MD! ///



# Set scene to Object Mode and deselect all.
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')

# Sets "uv_5" to active UV selection, and enables it. If UVs are broken, edit this. Edit UVs manually if it's a mix.
bpy.context.object.data.uv_layers['uv_5'].active = True
bpy.context.object.data.uv_layers['uv_5'].active_render = True
    
# Join all separated objects into one object.
bpy.ops.object.select_all()
bpy.ops.object.join()  

# Rotates collection, and applies scale.
bpy.ops.transform.rotate(use_proportional_edit=True, orient_axis='X', value=-2.739)
bpy.ops.transform.shear(orient_axis='X', value=-0.968)
bpy.ops.object.transform_apply(scale=True)

# Skews mesh data to be "normal."
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.transform.shear(orient_axis='X',value=-0.991)
bpy.ops.object.mode_set(mode='OBJECT')

# Corrects scale inconsistencies.
bpy.ops.transform.resize(value=(0.4, 0.6, 1.0))
bpy.ops.object.transform_apply(scale=True)

# Sets texture extensions to "Mirror." Many textures use mirroring, and are only half-textures in imported files.
for mat in bpy.data.materials:
    if mat.node_tree:
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                node.interpolation = 'Linear'
                node.extension = 'MIRROR'                
                from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
                
# Sets blending mode to "Hashed," and connects alpha channel to BSDF for functional transparency.
for collection in bpy.data.collections:
    for obj in collection.objects:
        if obj.type == 'MESH' and not obj.active_material == None:
            for item in obj.material_slots:
                mat = bpy.data.materials[item.name]
                if mat.use_nodes:                    
                    mat.blend_method = 'HASHED'
                    shader = mat.node_tree.nodes['Principled BSDF']
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            mat.node_tree.links.new(shader.inputs['Alpha'], node.outputs['Alpha'])
                        
# Done! :)