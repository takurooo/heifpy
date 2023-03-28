# -----------------------------------
# import
# -----------------------------------
from typing import List

from heifpy.file import BinaryFileReader

from . import boxutils
from .basebox import FullBox
from .infebox import ItemInfoEntry


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------


class ItemInformationBox(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘iinf’
    Container: Meta Box (‘meta’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self):
        super(ItemInformationBox, self).__init__()
        self.infe_list = []
        self.item_id_list = []  # 後で使う用

    def parse(self, reader: BinaryFileReader) -> None:
        super(ItemInformationBox, self).parse(reader)

        if self.get_version() == 0:
            entry_count = reader.read16()
        else:
            entry_count = reader.read32()

        self.infe_list = []
        self.item_id_list = []
        for _ in range(entry_count):
            box_size, box_type = boxutils.read_box_header(reader)
            if box_type == "infe":
                infe = ItemInfoEntry()
                infe.parse(reader)

                self.item_id_list.append(infe.item_ID)  # 後で使う用
                self.infe_list.append(infe)

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super(ItemInformationBox, self).print_box()
        print("entry_count :", len(self.infe_list))
        for infe in self.infe_list:
            infe.print_box()

    def get_item_id_list(self) -> List[int]:
        return self.item_id_list

    def get_item_type(self, item_ID: int) -> str:
        assert item_ID in self.item_id_list, "invalid item id"
        for infe in self.infe_list:
            if infe.item_ID == item_ID:
                return infe.item_type
        return ""


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
