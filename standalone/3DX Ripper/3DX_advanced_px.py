import bpy


#                              [ Written for Blender 4.1, using NinjaRipper 2.8 ]

# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 
#                                                                                                                     #
#     [[[[[ THIS SCRIPT *ADDITIONALLY* MAKES TEXTURES PIXELATED, MERGES VERTEXES, AND TUNES SHADERS VALUES! ]]]]]     #
#                                                                                                                     #
# @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ @ 

#                            /// RUNNING THIS SCRIPT ASSUMES YOU HAVE READ READ.MD! ///



# Scene Compatibility hack.
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all()
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_all()

# Rotates the mesh.
bpy.ops.transform.rotate(value=-1.39626, orient_axis='X')

# Skews the mesh.
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action = 'SELECT')
bpy.ops.transform.shear(orient_axis='X',value=-2.746)
bpy.ops.object.mode_set(mode='OBJECT')

# Corrects scaling and flips model.
bpy.ops.object.transform_apply(scale=True)
bpy.ops.transform.resize(value=(1, 1, 2.87991))
bpy.ops.transform.resize(value=(-1, 1, 1))
bpy.ops.object.transform_apply(scale=True)

# Shrinks model, applies scale to center of geometry, sends it to the center, and applies scale for compatability.
bpy.ops.transform.resize(value=(0.01,0.01,0.01))
bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
bpy.ops.object.location_clear(clear_delta=False)

# Merge duplicated and disconnected vertexes.
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action = 'SELECT')
bpy.ops.mesh.remove_doubles(threshold=0.0001)
bpy.ops.object.mode_set(mode='OBJECT')






# Sets texture extensions to "Mirror." Many textures use mirroring, and are only half-textures in imported files.
for mat in bpy.data.materials:
    if mat.node_tree:
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                node.interpolation = 'Closest'
                node.extension = 'MIRROR'                
                from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
                
# Sets blending mode to "Clip," and connects alpha channel to BSDF for functional transparency.
for collection in bpy.data.collections:
    for obj in collection.objects:
        if obj.type == 'MESH' and not obj.active_material == None:
            for item in obj.material_slots:
                mat = bpy.data.materials[item.name]
                if mat.use_nodes:                    
                    mat.blend_method = 'CLIP'
                    shader = mat.node_tree.nodes['Principled BSDF']
                    for node in mat.node_tree.nodes:
                        if node.type == 'TEX_IMAGE':
                            mat.node_tree.links.new(shader.inputs['Alpha'], node.outputs['Alpha'])

# Sets Metallic, Roughness, and IOR to values similar to those found in-game.
#ROUGHNESS
for mat in bpy.data.materials:
    if hasattr(mat.node_tree, "nodes"):
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                for input in node.inputs:
                    if input.name == 'Roughness':
                        input.default_value = 1
#METALLIC
for mat in bpy.data.materials:
    if hasattr(mat.node_tree, "nodes"):
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                for input in node.inputs:
                    if input.name == 'Metallic':
                        input.default_value = 0
#IOR                     
for mat in bpy.data.materials:
    if hasattr(mat.node_tree, "nodes"):
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                for input in node.inputs:
                    if input.name == 'IOR':
                        input.default_value = 1