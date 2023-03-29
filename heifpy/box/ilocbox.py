from typing import List, Optional

from heifpy.file import BinaryFileReader

from .basebox import FullBox


class ItemLocationExtent:
    def __init__(self):
        self.extent_offset = 0
        self.extent_length = 0
        self.extent_index = 0

    def get_extent_offset(self) -> int:
        return self.extent_offset

    def get_extent_length(self) -> int:
        return self.extent_length


class ItemLocation:
    CONSTRUCTION_METHOD_FILE_OFFSET = 0
    CONSTRUCTION_METHOD_IDAT_OFFSET = 1
    CONSTRUCTION_METHOD_ITEM_OFFSET = 2

    def __init__(self):
        self.item_ID = 0
        self.construction_method = 0
        self.data_reference_index = 0
        self.base_offset = 0
        self.item_loc_ext_list = []

    def get_item_ID(self) -> int:
        return self.item_ID

    def get_construction_method(self) -> int:
        return self.construction_method

    def get_base_offset(self) -> int:
        return self.base_offset

    def get_extent_list(self) -> List[ItemLocationExtent]:
        return self.item_loc_ext_list


class ItemLocationBox(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘iloc’
    Container: Meta box (‘meta’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self):
        super().__init__()
        self.offset_size = None
        self.length_size = None
        self.base_offset_size = None
        self.index_size = 0
        self.item_loc_list = []

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        tmp = reader.read16()
        # offset_size is taken from the set {0, 4, 8} and
        #  indicates the length data bytes of the offset field.
        self.offset_size = (tmp & 0xF000) >> 12
        # length_size is taken from the set {0, 4, 8} and
        #  indicates the length data bytes of the length field.
        self.length_size = (tmp & 0x0F00) >> 8
        # base_offset_size is taken from the set {0, 4, 8} and
        #  indicates the length data bytes of the base_offset field.
        self.base_offset_size = (tmp & 0x00F0) >> 4

        if self.get_version() == 1 or self.get_version() == 2:
            self.index_size = tmp & 0x000F
        else:
            # reversed = data & 0x000f
            self.index_size = 0

        if self.get_version() < 2:
            item_count = reader.read16()
        else:
            item_count = reader.read32()

        for _ in range(item_count):
            item_loc = ItemLocation()

            if self.get_version() < 2:
                item_loc.item_ID = reader.read16()
            elif self.get_version() == 2:
                item_loc.item_ID = reader.read32()

            if self.get_version() == 1 or self.get_version() == 2:
                tmp = reader.read16()
                # reversed = (data & 0xfff0) >> 4
                item_loc.construction_method = tmp & 0x000F  # 0:file 1:idat 2:item
            else:
                item_loc.construction_method = 0  # 0:file 1:idat 2:item

            item_loc.data_reference_index = reader.read16()
            item_loc.base_offset = reader.readn(self.base_offset_size * 8)

            extent_count = reader.read16()
            for _ in range(extent_count):
                item_loc_ext = ItemLocationExtent()

                if (
                    self.get_version() == 1 or self.get_version() == 2
                ) and 0 < self.index_size:
                    item_loc_ext.extent_index = reader.readn(self.index_size * 8)
                item_loc_ext.extent_offset = reader.readn(self.offset_size * 8)
                item_loc_ext.extent_length = reader.readn(self.length_size * 8)

                item_loc.item_loc_ext_list.append(item_loc_ext)

            self.item_loc_list.append(item_loc)

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print("offset_size :", self.offset_size)
        print("length_size :", self.length_size)
        print("base_offset_size :", self.base_offset_size)
        print("item_count :", len(self.item_loc_list))
        for item_iloc in self.item_loc_list:
            print("\titem_ID :", item_iloc.item_ID)
            print("\t\tconstruction_method  :", item_iloc.construction_method)
            print("\t\tdata_reference_index :", item_iloc.data_reference_index)
            print("\t\tbase_offset          :", item_iloc.base_offset)
            print("\t\textent_count         :", len(item_iloc.item_loc_ext_list))
            for item_iloc_ext in item_iloc.item_loc_ext_list:
                print("\t\t\textent_offset :", item_iloc_ext.extent_offset)
                print("\t\t\textent_length :", item_iloc_ext.extent_length)
                print("\t\t\textent_index  :", item_iloc_ext.extent_index)

    def get_item_loc(self, item_ID: int) -> Optional[ItemLocation]:
        for item_loc in self.item_loc_list:
            if item_loc.item_ID == item_ID:
                return item_loc

        assert 0, f"invalid item_ID {item_ID}"

    def has_item_id_entry(self, item_ID: int) -> bool:
        for item_loc in self.item_loc_list:
            if item_loc.item_ID == item_ID:
                return True

        return False


if __name__ == "__main__":
    pass
