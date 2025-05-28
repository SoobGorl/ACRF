import bpy


#                              [ Written for Blender 4.1, using 3DX Ripper ]

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

# Shrinks model, applies scale to center of geometry, sends it to the center, and applies scale for compatability.

# Resizes model to adjust for deformaties.





    

