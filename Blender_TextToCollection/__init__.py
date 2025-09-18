bl_info = {
    "name": "Collection Tools - CSV/YAML/Indented Collection Creator",
    "author": "'Javelin-prog' Jérôme Noël",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "Properties > Scene > Collection Importer",
    "description": "Create nested (or not nested) collections from CSV, YAML, or indented text",
    "category": "Object",
    "doc_url": "https://github.com/Javelin-prog/Blender_TextToCollection",
    "tracker_url": "https://github.com/Javelin-prog/Blender_TextToCollection/issues",
}

import bpy
import sys, os

# Path to the bundled "external" folder
addon_dir = os.path.dirname(__file__)
ext_dir = os.path.join(addon_dir, "external")

# Ensure the external directory is in sys.path
if ext_dir not in sys.path:
    sys.path.insert(0, ext_dir)


# Register and Unregister
def register():
    
    from . import TextToCollection
    TextToCollection.register()

def unregister():
    
    from . import TextToCollection
    TextToCollection.unregister()

if __name__ == "__main__":
    register()