# Blender – CSV / YAML / Indented Collection Creator

Import hierarchical collection structures into Blender from a **CSV**, **YAML**, or **Indented text file**.  
Quickly set up multiple collections or nested hierarchies with one click.

## IMPORTANT : 
- **Each Collection name must be UNIQUE** (and yes, even if they don't share the same parent) !
this is a blender limitation that  I can't change.

## Features

- Import from **CSV** with multiple columns (columns = hierarchy levels)  
- Import from **YAML** files for flexible nested tree definitions  
- Import from **Indented text** files (spaces or tabs define hierarchy)  
- Automatically creates **nested collections** in Blender’s Outliner  
- Prevents duplicates by reusing existing collections when possible  
- Works directly in the **Scene properties panel**  

## Installation

1. Download the zip file from the [latest release](https://github.com/Javelin-prog/Blender_Collection_Importer/releases/tag/stable-release)  
2. Open Blender  
3. Go to `Edit` > `Preferences` > `Add-ons` > `drop-down arrow`  
4. Click `Install...` and select the ZIP file you downloaded  
5. Enable the addon by checking the box  

::: primary
3 - 4 alternative. directly **drag and drop** the .zip file into the Blender window
:::

## Location 

`Properties Editor` > `Scene` > `Collection Importer`

## Usage

1. Enable the add-on in Blender preferences  
2. In the **Scene Properties**, locate the **Collection Importer panel**  
3. Click **Import CSV / YAML / Indented** and choose your file  
4. Collections are created automatically inside the active Scene collection

### File Formats

- **CSV**  
  - First row = parent collections (headers)  
  - Subsequent rows = children, one level per column  
  - Example:  

    ```csv
    parentCollection1,parentCollection2,parentCollection3
    childP1, ChildP2, ChildP3
    childP1.2, childP2.2, childP3.2
    ```

- **YAML**  
  - Uses nested lists and mappings  
  - Example:  

    ```yaml
    p1:
      - child1
      - child2
    p2:
      - child1
      - child2
    ```

- **Indented text**  
  - Each line = collection  
  - Indentation = hierarchy level (spaces or tabs)  
  - Example:  

    ```
    p1
      child1
      child2
    p2
      child1
      child2
    ```

## Notes

- Existing collections are reused — no accidental duplicates  
- You can mix flat and nested definitions in the same file  
- Works best if your input files are cleanly structured with consistent indentation  

## License

MIT License

