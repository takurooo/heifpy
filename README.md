# heifpy

Reader for High Efficiency Image File Format (HEIF)

Read and parse HEIF file for Python.

- reader for HEIF file.
- extracting information of HEIF file.
- not support image sequence.

# Usage

### How to use example

- #### Demux HEIF

```
python heif_demux.py <HEIF file>
```

Demux HEIF file and save items.

- #### Parse HEIF

```
python heif_parse.py <HEIF file>
```

Display box information in HEIF file.

### How to use HeifReader module

```python
import heifpy
heif_reader = heifpy.HeifReader(heif_path) # Parse HEIF file
```

HeifReader functions

| function name                       |                                                                         |
| ----------------------------------- | ----------------------------------------------------------------------- |
| get_major_brand()                   | Get major version from the FileTypeBox.                                 |
| get_minor_version()                 | TGet minor version from the FileTypeBox.D                               |
| get_compatible_brands()             | Get list of compatible brand from the FileTypeBox.                      |
| get_item_id_list()                  | Get list of item id from the ItemInformationBox.                        |
| get_item_id_list_by_type(item_type) | Get list of item id from the ItemInformationBox by item type.           |
| get_primary_item_id()               | Get primary item id from the PrimaryItemBox.                            |
| get_item_type(item_id)              | Get item type from the ItemInformationBox by item id.                   |
| get_item_properties(item_id)        | Get item properties from the ItemPropertiesBox by item id.              |
| get_item_offsets_sizes(item_id)     | Get list of location from the ItemLocationBox by item id.               |
| get_item_width_height(item_id)      | Get list of resolution from the ImageSpatialExtentsProperty by item id. |
| read_item(item_id)                  | Get item binary data by item id.                                        |
| print_boxes()                       | Display box information.                                                |
