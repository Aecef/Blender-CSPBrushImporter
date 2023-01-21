bl_info = {
    "name": "CSP Brush Importer",
    "author": "Aecef",
    "blender": (2, 80, 0),
    "version": (0, 5),
    "location": "View3D > Properties Panel > Texture > CSP Brush Import Panel",
    "description": "Imports A .SUT Brush As A Texture Paint Brush ",
    "warning": "Generates the image for the texture, but there are problems reading the PNG file. Currently fixed by resaving the png on the computer then reloading the image in the texture panel",
    "doc_url": "https://github.com/Aecef/Blender-CSPBrushImporter",
    "category": "3D View"
}


import bpy 
import os 
import sqlite3
from bpy.types import Brush
from bpy.props import StringProperty, BoolProperty 
from bpy_extras.io_utils import ImportHelper 
from bpy.types import Operator

def get_last_pos(str, source):
    str_find = bytearray(str,'ascii')
    last_pos = 0
    pos = 0
    while True:
        pos = source.find(str_find, last_pos)
        if pos == -1:
            break
        last_pos = pos + 1
    return (last_pos - 1)


def extract_png(sql_layer):
    try:
        with open(sql_layer, "rb") as inputFile:
            content = inputFile.read()
            if content != "":
                s = 'PNG'
                begin_pos = get_last_pos(s, content)
                begin_pos -= 1

                s = 'IEND'
                end_pos = get_last_pos(s, content)
                end_pos += 4

                with open(sql_layer[:sql_layer.find('.')]+".png", 'wb') as outputFile:
                    outputFile.write(content[begin_pos:end_pos])
    except FileNotFoundError:
        print("File not found")


def obtain_layers(sut_file_path):
    con = sqlite3.connect(sut_file_path)
    cursor = con.cursor()
    cursor.execute("select _PW_ID, FileData from MaterialFile")
    row = cursor.fetchone()
    
    while row != None:
      
        file_name = sut_file_path+"."+str(row[0])+".layer"
        
        with open(file_name, 'wb') as outputFile:
            outputFile.write(row[1])
            extract_png(file_name)
        os.remove(file_name)
        row = cursor.fetchone()
        
    cursor.close()

class FileBrowser(Operator, ImportHelper): 
    
    bl_idname = "test.file_browser" 
    bl_label = "Open the file browser" 
    
    filter_glob: StringProperty( 
        default='*.sut', 
        options={'HIDDEN'} 
        ) 

    def execute(self, context): 
        """Do something with the selected file(s).""" 

        filename, extension = os.path.splitext(self.filepath) 
        
        filename = filename[filename.rfind("\\")+1:]
        obtain_layers(self.filepath)
        
        # create a new image brush
        brush = bpy.data.brushes.new(name=filename, mode="TEXTURE_PAINT")
        
        # obtain the created image file
        image = bpy.data.images.load(self.filepath[:-3]+"png")
        
        
        image_texture = bpy.data.textures.new(name=filename, type= "IMAGE")
        bpy.data.brushes[filename].texture_slot.map_mode = 'VIEW_PLANE'
        
        # Scales the XYZ of the texture 
        #bpy.data.brushes[filename].texture_slot.scale[0] = 0.01
        #bpy.data.brushes[filename].texture_slot.scale[1] = 0.01
        #bpy.data.brushes[filename].texture_slot.scale[2] = 0.01

        # set the png to the brushes image
        image_texture.image = image
        bpy.data.brushes[filename].texture = image_texture
        
        return {'FINISHED'}


# Button To Add Brush
class AddBrush(bpy.types.Operator):
    """Button to look for a SUT File"""
    bl_idname = "brush.add"
    bl_label = "Add Brush"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        brush_lookup()
        return {'FINISHED'}

class CSP_Panel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "CSP Brush Import Panel"
    bl_idname = "CSP_IMPORT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "texture"


    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Add Brush Button
        layout.label(text="Import CSP Brush")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("brush.add")


def register():
    bpy.utils.register_class(FileBrowser)
    bpy.utils.register_class(CSP_Panel)
    bpy.utils.register_class(AddBrush)

def unregister():
    bpy.utils.unregister_class(FileBrowser)
    bpy.utils.unregister_class(CSP_Panel)
    bpy.utils.unregister_class(AddBrush)
    
def brush_lookup():
    bpy.ops.test.file_browser('INVOKE_DEFAULT')

if __name__ == "__main__":
    register()