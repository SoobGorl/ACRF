bl_info = {
    "name": "Animal Crossing Ripper Fixer",
    "author": "Soup Girl, Salvage",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "location": "3D Viewport > Sidebar > AC:RF",
    "description": "Cleans up 3DX and NinjaRipper Scenerips.",
    "category": "Porting",
    "wiki_url": "https://github.com/SoobGorl/ACRF"
}

import bpy
import math
import bmesh

# //////////////////////////////////////////////////////////////////// NINJA RIPPER SECTION

# Executes NinjaRipper mesh alterations to align/resize/rotate mesh objects to be "normal."
class OPERATOR_NR_meshfix(bpy.types.Operator):
    bl_idname = "mesh.nrfix"
    bl_label = "NR Meshfix"
    def execute(self,context):
        
        # Scene compatibility hack to run script, regardless if script is ran in edit mode, or without an active object.
        if len(bpy.context.scene.objects) == 0:
            return {"FINISHED"}
                    
        bpy.context.view_layer.objects.active = bpy.context.scene.objects[0]
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        # Sets UV to "uv_5" and renders it. If >ALL< UVs are broken, edit this. Edit UVs manually if it's a mix.
        if 'uv_5' in bpy.context.object.data.uv_layers:
            bpy.context.object.data.uv_layers['uv_5'].active = True
            bpy.context.object.data.uv_layers['uv_5'].active_render = True
            
        # Joins all separated objects into one mesh, as 3DX and NR meshes are a tossup.
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

        # Resizes collection to be about villager viewing height.
        bpy.ops.transform.resize(value=(0.04, 0.04, 0.04))
        bpy.ops.object.transform_apply(scale=True)

        # Transforms object closer to 3D Grid's origin.
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        bpy.ops.object.location_clear(clear_delta=False)

        # Merge duplicated and disconnected vertexes, and shades smooth. Remove lines 64-68 if this creates issues.
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.faces_shade_smooth()
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.object.mode_set(mode='OBJECT')
        )

        return {"FINISHED"}

# //////////////////////////////////////////////////////////////////// 3DX RIPPER SECTION
    
# Executes 3DX Ripper mesh alterations to align/resize/rotate mesh objects to be "normal."
class OPERATOR_3DX_meshfix(bpy.types.Operator):
    bl_idname = "mesh.3dxfix"
    bl_label = "3DX Meshfix"
    def execute(self,context):
        
        if len(bpy.context.scene.objects) == 0:
            return {"FINISHED"}
                    
        bpy.context.view_layer.objects.active = bpy.context.scene.objects[0]
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        
        # Slight hack.
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

        # Merge duplicated and disconnected vertexes, and shades smooth. Remove lines 115-119 if this creates issues.
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.faces_shade_smooth()
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        return {"FINISHED"}
    
# //////////////////////////////////////////////////////////////////// TEXTURE SECTION

# Sets Metallic, Roughness, and IOR to values similar to those found in-game.
def bsdf_mod(mat):
    if hasattr(mat.node_tree, "nodes"):
        for node in mat.node_tree.nodes:
            if node.type == 'BSDF_PRINCIPLED':
                for input in node.inputs:
                    if input.name == 'Roughness':
                        input.default_value = 1 # Roughness Value
                    if input.name == 'Metallic':
                        input.default_value = 0 # Metallic Value (unused, but for compatibility).
                    if input.name == 'IOR':
                        input.default_value = 1 # IOR Value

# BSDF Button, executes above.
class OPERATOR_bsdftweak(bpy.types.Operator):
    bl_idname = "texture.bsdftweak"
    bl_label = "BSDF Tweaks"
    def execute(self,context):
        for mat in bpy.data.materials:
            bsdf_mod(mat)

        return {"FINISHED"}

# Sets texture extension to "Mirror." Many textures are only half-textures, and this applies mirroring to all textures.
# Change extensions MANUALLY (repeat, etc) if there are edgecases you encounter.
class OPERATOR_mirror(bpy.types.Operator):
    bl_idname = "texture.mirror"
    bl_label = "Mirror"
    def execute(self,context):   
        #MIRROR
        for mat in bpy.data.materials:
            if mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        node.extension = 'MIRROR'                
                        from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
                        
        return {"FINISHED"}

# Sets texture interpolation to Closest, and sets transparency to Alpha Clip (+ plugs in alpha channels) for ALL textures.
class OPERATOR_closest(bpy.types.Operator):
    bl_idname = "texture.closest"
    bl_label = "closest"
    def execute(self,context):   
        # Closest/Nearest Neighbor/Pixel Interpolation
        for mat in bpy.data.materials:
            if mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        node.interpolation = 'Closest' # Texture Interpolation         
                        from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
        # Alpha Clip + Alpha Channel Routing
        for collection in bpy.data.collections:
            for obj in collection.objects:
                if obj.type == 'MESH' and not obj.active_material == None:
                    for item in obj.material_slots:
                        mat = bpy.data.materials[item.name]
                        if mat.use_nodes:                    
                            mat.blend_method = 'CLIP' # Alpha Mode
                            shader = mat.node_tree.nodes['Principled BSDF']
                            for node in mat.node_tree.nodes:
                                if node.type == 'TEX_IMAGE':
                                    mat.node_tree.links.new(shader.inputs['Alpha'], node.outputs['Alpha'])
                                    
        return {"FINISHED"}
    
# Sets texture interpolation to Linear, and sets transparency to Alpha Hashed (+ plugs in alpha channels) for ALL textures.
class OPERATOR_linear(bpy.types.Operator):
    bl_idname = "texture.linear"
    bl_label = "linear"
    def execute(self,context):   
        # Linear/Blurry Texture Interpolation
        for mat in bpy.data.materials:
            if mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        node.interpolation = 'Linear' # Texture Interpolation            
                        from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
        # Alpha Hashed + Alpha Channel Routing
        for collection in bpy.data.collections:
            for obj in collection.objects:
                if obj.type == 'MESH' and not obj.active_material == None:
                    for item in obj.material_slots:
                        mat = bpy.data.materials[item.name]
                        if mat.use_nodes:                    
                            mat.blend_method = 'HASHED' # Alpha Mode
                            shader = mat.node_tree.nodes['Principled BSDF']
                            for node in mat.node_tree.nodes:
                                if node.type == 'TEX_IMAGE':
                                    mat.node_tree.links.new(shader.inputs['Alpha'], node.outputs['Alpha'])
                                    
        return {"FINISHED"}
    
# //////////////////////////////////////////////////////////////////// EXTRAS SECTION

# ////// SHADOW

# Selected meshes have their materials selected, and defined. This is used for changing multiple selected shadow materials,
# so they don't have to be parsed one at a time.
def get_selected_materials():    
    obj = bpy.context.edit_object
    if obj is None or obj.type != 'MESH':
        return []

    mesh = bmesh.from_edit_mesh(obj.data)
    selected_materials = set()

    for face in mesh.faces:
        if face.select:
            material_index = face.material_index
            if material_index < len(obj.material_slots):
                material = obj.material_slots[material_index].material
                if material:
                    selected_materials.add(material)

    return list(selected_materials)

# Creates Color Ramp nodes and sets them to black, so shadows look dark instead of white (well, whatever is selected).
class OPERATOR_shadow(bpy.types.Operator):
    bl_idname = "extra.shadow"
    bl_label = "shadow"
    def execute(self,context):
        for mat in get_selected_materials():

            color = [
            (0x000000, 1),  # red = 231, green = 98, blue = 84, alpha = 1, allow lower case
            (0x000000, 1),
            ]

            def to_blender_color(c):    # gamma correction
                c = min(max(0, c), 255) / 255
                return c / 12.92 if c < 0.04045 else math.pow((c + 0.055) / 1.055, 2.4)

            blend_color = [(
                to_blender_color(c[0] >> 16),
                to_blender_color(c[0] >> 8 & 0xff), 
                to_blender_color(c[0] & 0xff),
                c[1]) for c in color]
            color_count = len(color)

            for e in blend_color:
                print(e)
                
            tree    = mat.node_tree
            nodes   = tree.nodes
            node    = nodes.new(type='ShaderNodeValToRGB') # add color ramp node

            ramp    = node.color_ramp
            el      = ramp.elements

            dis     = 1 / (color_count - 1)
            x       = dis
            for r in range(color_count - 2):
                el.new(x)
                x += dis

            for i, e in enumerate(el):
                e.color = blend_color[i]
                
            nodes["Color Ramp"].color_ramp.elements[1].position = 0.313636
            # Defines Color Ramp/Principled BSDF Inputs/Outputs
            nodes['Color Ramp']
            nodes['Color Ramp'].color_ramp.elements[1].color = (0, 0, 0, 1)
            nodes['Color Ramp'].outputs[0]
            nodes['Principled BSDF'].inputs[0]
            nodes['Principled BSDF'].inputs['Base Color']
            # Connects Color Ramp/Principled BSDF
            tree.links.new(
                nodes['Color Ramp'].outputs['Color'],
                nodes['Principled BSDF'].inputs['Base Color']
            )
            
        return {"FINISHED"}

# ////// WATER
# Similar Color Ramp setup to the Shadow nodes.
class OPERATOR_water(bpy.types.Operator):
    bl_idname = "extra.water"
    bl_label = "water"
    def execute(self,context):
        for mat in get_selected_materials():

            color = [
            (0x1000D1, 1),  # red = 231, green = 98, blue = 84, alpha = 1, allow lower case
            (0xFFFFFF, 1),
            ]

            def to_blender_color(c):    # gamma correction
                c = min(max(0, c), 255) / 255
                return c / 12.92 if c < 0.04045 else math.pow((c + 0.055) / 1.055, 2.4)

            blend_color = [(
                to_blender_color(c[0] >> 16),
                to_blender_color(c[0] >> 8 & 0xff), 
                to_blender_color(c[0] & 0xff),
                c[1]) for c in color]
            color_count = len(color)

            for e in blend_color:
                print(e)
                
            tree    = mat.node_tree
            nodes   = tree.nodes
            node    = nodes.new(type='ShaderNodeValToRGB') # add color ramp node

            ramp    = node.color_ramp
            el      = ramp.elements

            dis     = 1 / (color_count - 1)
            x       = dis
            for r in range(color_count - 2):
                el.new(x)
                x += dis

            for i, e in enumerate(el):
                e.color = blend_color[i]
                
            nodes["Color Ramp"].color_ramp.elements[1].position = 0.313636

            # Created new Principled BSDF node as a hacky fix to a bug.
            nodes.new(type="ShaderNodeBsdfPrincipled")

            # Defines Color Ramp/Principled BSDF Inputs/Outputs
            nodes['Color Ramp']
            nodes['Color Ramp'].color_ramp.elements[1].color = (1, 1, 1, 1)
            nodes['Color Ramp'].outputs[0]
            nodes['Principled BSDF'].inputs[0]
            nodes['Principled BSDF'].inputs['Base Color']
            # Connects Color Ramp/Principled BSDF
            tree.links.new(
                nodes['Color Ramp'].outputs['Color'],
                nodes['Principled BSDF'].inputs['Base Color']
            )
            
            # Defines Color Ramp/Image Texture Inputs/Outputs
            tree.nodes['Image Texture']
            nodes['Image Texture'].outputs[0]
            nodes['Color Ramp'].inputs[0]
            nodes['Color Ramp'].inputs['Fac']
            # Connects Color Ramp/Image Texture
            tree.links.new(
                nodes['Image Texture'].outputs['Color'],
                nodes['Color Ramp'].inputs['Fac']
            )
            
            # Creates a Transparent BSDF node for water transparency
            nodes.new(type='ShaderNodeBsdfTransparent')
            # Creates a Mix Shader node for mixing water transparency and the image.
            nodes.new(type='ShaderNodeMixShader')

            # Defines Principled BSDF/Mix Shader Inputs/Outputs
            nodes['Principled BSDF']
            nodes['Principled BSDF'].outputs[0]
            nodes['Mix Shader'].inputs[1]
            nodes['Mix Shader'].inputs['Shader']
            # Connects Principled BSDF/Mix Shader
            tree.links.new(
                nodes['Principled BSDF'].outputs['BSDF'],
                nodes['Mix Shader'].inputs['Shader']
            )
            
            # Defines Transparent BSDF/Mix Shader Inputs/Outputs
            nodes['Transparent BSDF']
            nodes['Transparent BSDF'].outputs[0]
            nodes['Mix Shader'].inputs[2]
            nodes['Mix Shader'].inputs['Shader_001']
            # Connects Transparent BSDF/Mix Shader
            tree.links.new(
                nodes['Transparent BSDF'].outputs['BSDF'],
                nodes['Mix Shader'].inputs['Shader_001']
            )

            # Defines Material Output/Mix Shader Inputs/Outputs
            nodes['Mix Shader']
            nodes['Mix Shader'].outputs[0]
            nodes['Material Output'].inputs[0]
            nodes['Material Output'].inputs['Surface']
            tree.links.new(
            # Connects Material Output/Mix Shader
                nodes['Mix Shader'].outputs['Shader'],
                nodes['Material Output'].inputs['Surface']
            )
            
            # Separates selection into its own object, and selects that new object as the active one for modifier applications.           
            org_obj_list = {obj.name for obj in context.selected_objects}
                        
            bpy.ops.mesh.separate(type = 'SELECTED')

            bpy.ops.object.editmode_toggle()
            for obj in context.selected_objects:
                if obj and obj.name in org_obj_list:
                    obj.select_set(False)
                else:
                    context.view_layer.objects.active = obj
                    
            # Applies Array Modifier with values typical to those ingame for a similar water look.
            bpy.ops.object.modifier_add(type='ARRAY')
            # Swap to constant offset, and set values.
            bpy.context.object.modifiers["Array"].use_relative_offset = False
            bpy.context.object.modifiers["Array"].use_constant_offset = True
            bpy.context.object.modifiers["Array"].constant_offset_displace[2] = -0.52
            bpy.context.object.modifiers["Array"].constant_offset_displace[0] = 0
            bpy.context.object.modifiers["Array"].offset_u = 0.380952
            bpy.context.object.modifiers["Array"].offset_v = -0.693878
            bpy.context.object.modifiers["Array"].count = 4

            # Changes Alpha/transparency mode to "BLEND". Change to "CLIP" or "HASHED" if either is desired.
            mat.blend_method = 'BLEND'
            
            # Calls from earlier in the script, and applies IOR/Metallic/Roughness values to look more water-y.
            bsdf_mod(mat)
            
            # Disconnects alpha socket that may have been applied with the "transparency" button.
            for node in nodes:
                if isinstance(node, bpy.types.ShaderNodeBsdfPrincipled):
                    for input_socket in node.inputs:
                        if input_socket.is_linked and input_socket.name == 'Alpha':
                            tree.links.remove(input_socket.links[0])
            
        return {"FINISHED"}
    

# ////// ZFIGHTING FIX
# Fixes 80% of issues relating to zfighting by applying a limited dissolve, backface culling, and flipping normals. YMMV.
class OPERATOR_zfight(bpy.types.Operator):
    bl_idname = "extra.zfight"
    bl_label = "zfight"
    def execute(self,context):
        #Applies only to selected materials/textures.
        for mat in get_selected_materials():
            # Applies a limited dissolve for selected materials.
            bpy.ops.mesh.dissolve_limited()
            # Flips normals for selected materials.
            bpy.ops.mesh.flip_normals()
            # Enables backface culling for selected materials.
            mat.use_backface_culling = True

        return {"FINISHED"}
    

# ////// SHADE SELECTED FLAT
# Shades selected parts of mesh in edit mode flat. May help for zfighting/"looking bad" issues.
class OPERATOR_flat(bpy.types.Operator):
    bl_idname = "extra.flat"
    bl_label = "flat"
    def execute(self,context):

        for obj in bpy.context.selected_objects:
            bpy.ops.mesh.faces_shade_flat()
            
        return {"FINISHED"}

# ////// SHADE SELECTED SMOOTH
# Shades selected parts of mesh in edit mode smooth.
class OPERATOR_smooth(bpy.types.Operator):
    bl_idname = "extra.smooth"
    bl_label = "smooth"
    def execute(self,context):

        for obj in bpy.context.selected_objects:
            bpy.ops.mesh.faces_shade_smooth()
            
        return {"FINISHED"}
    
# //////////////////////////////////////////////////////////////////// UI SECTION

class ACRFPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AC:RF"
    bl_label = "Animal Crossing Ripper Fixer"
    bl_options = {"HEADER_LAYOUT_EXPAND"}

class acrf_main(ACRFPanel, bpy.types.Panel):
    bl_idname = "acrf_main"
    bl_label = "AC:RF"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Animal Crossing Ripper Fixer")

class meshfix(ACRFPanel, bpy.types.Panel):
    bl_parent_id = "acrf_main"
    bl_label = "Mesh Fixes (NR/3DX)"
    

    def draw(self, context):
        layout = self.layout
        self.layout.separator()
        layout.operator("mesh.nrfix", text="NinjaRipper Mesh fix", icon="SURFACE_DATA")
        self.layout.separator()
        layout.operator("mesh.3dxfix", text="3DX Ripper Mesh fix", icon="SURFACE_DATA")
        self.layout.separator()
        layout=self.layout

class texturefix(ACRFPanel, bpy.types.Panel):
    bl_parent_id = "acrf_main"
    bl_label = "Texture Fixes + Tweaks"

    def draw(self, context):
        layout = self.layout
        self.layout.separator()
        layout.operator("texture.bsdftweak", text="BSDF Tweaks", icon="MATERIAL_DATA")
        self.layout.separator()
        layout.operator("texture.mirror", text="Texture Mirror", icon="MOD_MIRROR")
        self.layout.separator()
        layout.operator("texture.closest", text="Closest + Alpha Clip", icon="IPO_CONSTANT")
        self.layout.separator()
        layout.operator("texture.linear", text="Linear + Alpha Hashed", icon="IPO_LINEAR")
        self.layout.separator()
        
class extras(ACRFPanel, bpy.types.Panel):
    bl_parent_id = "acrf_main"
    bl_label = "Extra (Shadows, Water, etc)"

    def draw(self, context):
        layout = self.layout
        layout.operator("extra.shadow", text="Selection - Shadows", icon="MOD_CAST")
        self.layout.separator()
        layout.operator("extra.water", text="Selection - Water Texture", icon="MATFLUID")
        self.layout.separator()
        layout.operator("extra.zfight", text="Selection - Zfighting Fix", icon="FILE_VOLUME")
        self.layout.separator()
        layout.operator("extra.flat", text="Selection - Shade Flat", icon="LIGHT_AREA")
        self.layout.separator()
        layout.operator("extra.smooth", text="Selection - Shade Smooth", icon="LIGHT_HEMI")
        self.layout.separator()

classes = (
    acrf_main,
    meshfix, 
    texturefix,
    extras,
    OPERATOR_NR_meshfix,
    OPERATOR_3DX_meshfix,
    OPERATOR_bsdftweak,
    OPERATOR_mirror,
    OPERATOR_closest,
    OPERATOR_linear,
    OPERATOR_shadow,
    OPERATOR_water,
    OPERATOR_zfight,
    OPERATOR_flat,
    OPERATOR_smooth
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()