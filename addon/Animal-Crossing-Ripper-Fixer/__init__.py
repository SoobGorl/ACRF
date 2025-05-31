bl_info = {
    "name": "Animal Crossing Ripper Fixer",
    "author": "Soup Girl",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D Viewport > Sidebar > AC:RF",
    "description": "Cleans up 3DX and NinjaRipper Scenerips.",
    "category": "Porting",
    "wiki_url": "https://github.com/SoobGorl/ACRF"
}

import bpy

# //////////////////////////////////////////////////////////////////// NR SECTION

# Executes NR mesh alterations
class OPERATOR_NR_meshfix(bpy.types.Operator):
    bl_idname = "mesh.nrfix"
    bl_label = "NR Meshfix"
    def execute(self,context):
        
        # Scene Compatibility hack.
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

        # Resizes collection to be about villager viewing height.  /////// DELETE LINES 42 - 48 IF OBJECT "DISAPPEARS!" ///////
        bpy.ops.transform.resize(value=(0.04, 0.04, 0.04))
        bpy.ops.object.transform_apply(scale=True)

        # Transforms object closer to 3D Grid's origin, and applies scale to object origin, calculating via surface.
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        bpy.ops.object.location_clear(clear_delta=False)

        # Merge duplicated and disconnected vertexes.
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action = 'SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.object.mode_set(mode='OBJECT')

        return {"FINISHED"}

# //////////////////////////////////////////////////////////////////// 3DX SECTION
    
# Executes 3DX mesh alterations
class OPERATOR_3DX_meshfix(bpy.types.Operator):
    bl_idname = "mesh.3dxfix"
    bl_label = "3DX Meshfix"
    def execute(self,context):
        
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
        
        return {"FINISHED"}
    
# //////////////////////////////////////////////////////////////////// TEXTURE SECTION

# Sets Metallic, Roughness, and IOR to values similar to those found in-game.
class OPERATOR_bsdftweak(bpy.types.Operator):
    bl_idname = "texture.bsdftweak"
    bl_label = "BSDF Tweaks"
    def execute(self,context):
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

        return {"FINISHED"}

# Sets texture extensions to "Mirror." Many textures use mirroring, and are only half-textures in imported files.
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

# Sets texture interpolation to Closest, and sets transparency to Alpha Clip (+ plugs in alpha channels).    
class OPERATOR_closest(bpy.types.Operator):
    bl_idname = "texture.closest"
    bl_label = "closest"
    def execute(self,context):   
        # Closest/Nearest Neighbor/Pixel Interpolation
        for mat in bpy.data.materials:
            if mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        node.interpolation = 'Closest'         
                        from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
        # Alpha Clip + Alpha Channel Routing
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
                                    
        return {"FINISHED"}
    
# Sets texture interpolation to Linear, and sets transparency to Alpha Hashed (+ plugs in alpha channels).  
class OPERATOR_linear(bpy.types.Operator):
    bl_idname = "texture.linear"
    bl_label = "linear"
    def execute(self,context):   
        # Linear/Blurry Texture Interpolation
        for mat in bpy.data.materials:
            if mat.node_tree:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        node.interpolation = 'Linear'         
                        from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
        # Alpha Hashed + Alpha Channel Routing
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
                                    
        return {"FINISHED"}
    
# //////////////////////////////////////////////////////////////////// UI SECTION

class HelloWorldPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AC:RF"
    bl_label = "Animal Crossing Ripper Fixer"
    bl_options = {"DEFAULT_CLOSED"}

class acrf_main(HelloWorldPanel, bpy.types.Panel):
    bl_idname = "acrf_main"
    bl_label = "AC:RF"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Animal Crossing Ripper Fixer :D")

class meshfix(HelloWorldPanel, bpy.types.Panel):
    bl_parent_id = "acrf_main"
    bl_label = "Mesh Fixes (NR/3DX)"

    def draw(self, context):
        layout = self.layout
        self.layout.separator()
        layout.operator("mesh.nrfix", text="NinjaRipper Mesh fix")
        self.layout.separator()
        layout.operator("mesh.3dxfix", text="3DX Ripper Mesh fix")
        self.layout.separator()

class texturefix(HelloWorldPanel, bpy.types.Panel):
    bl_parent_id = "acrf_main"
    bl_label = "Texture Fixes + Tweaks"

    def draw(self, context):
        layout = self.layout
        self.layout.separator()
        layout.operator("texture.bsdftweak", text="BSDF Tweaks")
        self.layout.separator()
        layout.operator("texture.mirror", text="Texture Mirror")
        self.layout.separator()
        layout.operator("texture.closest", text="Closest + Alpha Clip")
        self.layout.separator()
        layout.operator("texture.linear", text="Linear + Alpha Hashed")
        self.layout.separator()
        
class extras(HelloWorldPanel, bpy.types.Panel):
    bl_parent_id = "acrf_main"
    bl_label = "Extra (Shadows, Water, etc)"

    def draw(self, context):
        layout = self.layout
        layout.label(text="")

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
    OPERATOR_linear
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()