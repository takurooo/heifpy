# -----------------------------------
# import
# -----------------------------------
from enum import Enum
from typing import List, Tuple

from .box import BoxReader, ItemProperty
from .file import BinaryFileReader


__all__ = ["ItemType", "HeifReader"]

# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------


class ItemType(Enum):
    HVC1 = "hvc1"
    GRID = "grid"
    EXIF = "Exif"
    XMP = "mime"


class HeifReader:
    """
    Class for reading HEIF file.

    Attributes
    ----------
    img_path : str
        File path of HEIF file.
    item_properties : dict
        Item properties associated with item.
    box_reader : BoxReader
        Reader for ISO Base Media File Format.
    box_reader : BinaryFileReader
        Reader for binary file。
    """

    def __init__(self, img_path: str):
        self.img_path = img_path

        self.item_properties = {}

        self.box_reader = BoxReader()
        self.binary_reader = BinaryFileReader(img_path)

        self.box_reader.read_boxes(self.binary_reader)
        self.binary_reader.seek(0)

        self._associate_item_property()

    def __del__(self):
        self.binary_reader.close()

    def _associate_item_property(self) -> None:
        ipma = self.box_reader.meta.iprp.ipma
        ipco = self.box_reader.meta.iprp.ipco

        prop_list = ipco.get_item_properties()
        for association in ipma.get_item_property_association():
            self.item_properties[association.item_ID] = []
            for prop_idx in association.property_index:
                prop = prop_list[prop_idx - 1]
                self.item_properties[association.item_ID].append(prop)

    def get_major_brand(self) -> str:
        """
        Get major version from the FileTypeBox.

        Returns
        -------
        major_version : str
            major version.
        """
        return self.box_reader.ftyp.get_major_brand()

    def get_minor_version(self) -> int:
        """
        Get minor version from the FileTypeBox.

        Returns
        -------
        minor_version : int
            minor version.
        """
        return self.box_reader.ftyp.get_minor_version()

    def get_compatible_brands(self) -> List[str]:
        """
        Get list of compatible brand from the FileTypeBox.

        Returns
        -------
        compatible_brands : list
            List of compatible brand.
        """
        return self.box_reader.ftyp.get_compatible_brands()

    def get_item_id_list(self) -> List[int]:
        """
        Get list of item id from the ItemInformationBox.

        Returns
        -------
        item_id_list : list
            List of item id.
        """
        return self.box_reader.meta.iinf.get_item_id_list()

    def get_item_id_list_by_type(self, item_type: ItemType) -> List[int]:
        """
        Get list of item id from the ItemInformationBox by item type.

        Parameters
        ----------
        item_type : ItemType
            Type of item.

        Returns
        -------
        item_id_list : list
            List of item id.
        """
        item_id_list = []
        for item_id in self.box_reader.meta.iinf.get_item_id_list():
            if item_type == self.get_item_type(item_id):
                item_id_list.append(item_id)
        return item_id_list

    def get_primary_item_id(self) -> int:
        """
        Get primary item id from the PrimaryItemBox.

        Returns
        -------
        primary_item_id : int
            Primary item id.
        """
        return self.box_reader.meta.pitm.get_primary_item_id()

    def get_item_type(self, item_id: int) -> str:
        """
        Get item type from the ItemInformationBox by item id.

        Parameters
        ----------
        item_id : int
            ID of item.

        Returns
        -------
        item_type : ItemType
            Type of item.
        """
        return self.box_reader.meta.iinf.get_item_type(item_id)

    def get_item_properties(self, item_id: int) -> List[ItemProperty]:
        """
        Get item properties from the ItemPropertiesBox by item id.

        Parameters
        ----------
        item_id : int
            ID of item.

        Returns
        -------
        item_properties : list
            List of item property.
        """
        return self.item_properties[item_id]

    def get_item_offsets_sizes(self, item_id: int) -> Tuple[List[int], List[int]]:
        """
        Get list of location from the ItemLocationBox by item id.

        Parameters
        ----------
        item_id : int
            ID of item.

        Returns
        -------
        location : list
            List of item location.
        """
        iloc = self.box_reader.meta.iloc
        assert iloc is not None, "iloc not found."
        assert iloc.has_item_id_entry(item_id), f"invali item id {item_id}"

        item_loc = iloc.get_item_loc(item_id)

        construction_method = item_loc.get_construction_method()
        base_offset = item_loc.get_base_offset()
        item_loc_ext_list = item_loc.get_extent_list()

        # TODO idat_offset と item_offset は未対応
        assert (
            construction_method == item_loc.CONSTRUCTION_METHOD_FILE_OFFSET
        ), f"constructionmethod not filetop {construction_method}"

        item_offset_list = []
        item_size_list = []
        for item_loc_ext in item_loc_ext_list:
            item_offset = base_offset + item_loc_ext.get_extent_offset()
            item_size = item_loc_ext.get_extent_length()

            item_offset_list.append(item_offset)
            item_size_list.append(item_size)

        return (item_offset_list, item_size_list)

    def get_item_width_height(self, item_id: int) -> Tuple[int, int]:
        """
        Get list of resolution from the ImageSpatialExtentsProperty by item id.

        Parameters
        ----------
        item_id : int
            ID of item.

        Returns
        -------
        reolution : tuple
            Tuple of item resolution.
        """
        for item_property in self.item_properties[item_id]:
            if item_property.get_type() == "ispe":
                ispe = item_property
                return ispe.get_image_width_height()

        return (0, 0)

    def read_item(self, item_id: int) -> bytes:
        """
        Get item binary data by item id.

        Parameters
        ----------
        item_id : int
            ID of item.

        Returns
        -------
        item : byte
            item data.
        """
        item_offset_list, item_size_list = self.get_item_offsets_sizes(item_id)
        item_data = b""
        for item_offset, item_size in zip(item_offset_list, item_size_list):
            self.binary_reader.seek(item_offset)
            item_data += self.binary_reader.read_raw(item_size)

        return item_data

    def print_boxes(self) -> None:
        """
        Display box information.
        """
        self.box_reader.print_boxes()


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
