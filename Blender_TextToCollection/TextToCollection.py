
import bpy
import csv
import os

from bpy.types import Operator, Panel
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

# --- Optional: YAML support ---
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# --- Utility: create or reuse collection ---
def get_or_create_collection(name, parent=None):
    if not name:
        return None
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        if parent:
            parent.children.link(col)
        else:
            bpy.context.scene.collection.children.link(col)
    return col

# --- Parser: CSV (multi-column tree) ---
def import_csv(filepath):
    with open(filepath, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        parents = [get_or_create_collection(h.strip()) if h.strip() else None for h in headers]

        for row in reader:
            parent = None
            for i, cell in enumerate(row):
                cell = cell.strip()
                if not cell:
                    continue
                parent = get_or_create_collection(cell, parents[i] if i == 0 else parent)

# --- Parser: YAML ---
def import_yaml(filepath):
    if not HAS_YAML:
        raise ImportError("PyYAML not available. Please install 'pyyaml' in Blender's Python.")
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    def build_tree(node, parent=None):
        if isinstance(node, dict):
            for k, v in node.items():
                col = get_or_create_collection(str(k), parent)
                build_tree(v, col)
        elif isinstance(node, list):
            for item in node:
                build_tree(item, parent)
        else:
            get_or_create_collection(str(node), parent)

    build_tree(data)

# --- Parser: Indentation-based text ---
def import_indented(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    stack = [(0, bpy.context.scene.collection)]  # (indent_level, collection)

    for line in lines:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" \t"))
        name = line.strip()

        # Find parent at correct level
        while stack and indent <= stack[-1][0]:
            stack.pop()

        parent = stack[-1][1] if stack else bpy.context.scene.collection
        new_col = get_or_create_collection(name, parent)
        stack.append((indent, new_col))

# --- Operator ---
class IMPORT_OT_collections(Operator, ImportHelper):
    bl_idname = "import_scene.collections_tree"
    bl_label = "Import Collections (CSV/YAML/Indented)"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".csv;.yaml;.yml;.txt"
    filter_glob: StringProperty(default="*.csv;*.yaml;*.yml;*.txt", options={'HIDDEN'})

    def execute(self, context):
        ext = os.path.splitext(self.filepath)[1].lower()

        try:
            if ext == ".csv":
                import_csv(self.filepath)
            elif ext in (".yaml", ".yml"):
                import_yaml(self.filepath)
            elif ext == ".txt":
                import_indented(self.filepath)
            else:
                self.report({'ERROR'}, f"Unsupported file type: {ext}")
                return {'CANCELLED'}
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {e}")
            return {'CANCELLED'}

        self.report({'INFO'}, "Collections created successfully.")
        return {'FINISHED'}

# --- UI ---
class VIEW3D_PT_collection_import(Panel):
    bl_label = "Collection Importer"
    bl_idname = "VIEW3D_PT_collection_import"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        layout.operator("import_scene.collections_tree", text="Import CSV / YAML / Indented")

def register():
    bpy.utils.register_class(IMPORT_OT_collections)
    bpy.utils.register_class(VIEW3D_PT_collection_import)

def unregister():
    bpy.utils.unregister_class(IMPORT_OT_collections)
    bpy.utils.unregister_class(VIEW3D_PT_collection_import)

if __name__ == "__main__":
    register()