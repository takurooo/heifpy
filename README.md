# heifpy

A High Efficiency Image File Format (HEIF) Reader for Python

This library allows you to read and parse HEIF files in Python.
It provieds the following functionality:

- Read HEIF files.
- Extract information from HEIF files.
- Note: Image sequences are not supported.

# Usage

### Example Usage

- #### Demux HEIF

```
python heif_demux.py <HEIF file>
```

Demux a HEIF file and save its items.

- #### Parse HEIF

```
python heif_parse.py <HEIF file>
```

Display box information contained in a HEIF file.

### How to use the HeifReader module

```python
import heifpy
heif_reader = heifpy.HeifReader(heif_path) # Parse HEIF file
```

HeifReader functions

| function name                       |                                                                         |
| ----------------------------------- | ----------------------------------------------------------------------- |
| get_major_brand()                   | Retrieve the major version from the FileTypeBox.                        |
| get_minor_version()                 | Retrieve minor version from the FileTypeBox.                            |
| get_compatible_brands()             | Retrieve a list of compatible brands from the FileTypeBox.              |
| get_item_id_list()                  | Retrieve a list of item IDs from the ItemInformationBox.                |
| get_item_id_list_by_type(item_type) | Retrieve a list of item IDs from the ItemInformationBox by item type.   |
| get_primary_item_id()               | Retrieve the primary item ID from the PrimaryItemBox.                   |
| get_item_type(item_id)              | Retrieve the item type from the ItemInformationBox by item ID.          |
| get_item_properties(item_id)        | Retrieve item properties from the ItemPropertiesBox by item ID.         |
| get_item_offsets_sizes(item_id)     | Retrieve a list of location from the ItemLocationBox by item ID.        |
| get_item_width_height(item_id)      | Retrieve a list of resolution from the ImageSpatialExtentsProperty by item ID. |
| read_item(item_id)                  | Retrieve item binary data by item ID.                                   |
| print_boxes()                       | Display box information.                                                |
