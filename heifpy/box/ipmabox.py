# -----------------------------------
# import
# -----------------------------------
from typing import List

from heifpy.file import BinaryFileReader

from .basebox import FullBox


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------


# -----------------------------------
# class
# -----------------------------------
class Association:
    def __init__(self):
        self.item_ID = 0
        self.essential = []
        self.property_index = []


class ItemPropertyAssociation(FullBox):
    """
    ISO/IEC 23008-12
    Box Type: ‘ipma’
    """

    def __init__(self):
        super(ItemPropertyAssociation, self).__init__()
        self.entry_cout = None
        self.association_count = None
        # self.item_ID = None
        # self.essential = None
        # self.property_index = None
        self.association_list = []

    def parse(self, reader: BinaryFileReader) -> None:
        super(ItemPropertyAssociation, self).parse(reader)

        self.entry_cout = reader.read32()

        self.association_list = []
        # self.item_ID = []
        # self.association_count = []
        # self.essential = [[] for _ in range(self.entry_cout)]
        # self.property_index = [[] for _ in range(self.entry_cout)]
        for i in range(self.entry_cout):
            association = Association()

            if self.get_version() < 1:
                # self.item_ID.append(reader.read16('big'))
                association.item_ID = reader.read16()
            else:
                # self.item_ID.append(reader.read32('big'))
                association.item_ID = reader.read32()

            association_count = reader.read8()
            for _ in range(association_count):
                if self.flags & 1:
                    tmp = reader.read16()
                    # self.essential[i].append((tmp & 0x8000) >> 15)
                    # self.property_index[i].append(tmp & 0x7fff)
                    association.essential.append((tmp & 0x8000) >> 15)
                    association.property_index.append(tmp & 0x7FFF)
                else:
                    tmp = reader.read8()
                    # self.essential[i].append((tmp & 0x80) >> 7)
                    # self.property_index[i].append(tmp & 0x7f)
                    association.essential.append((tmp & 0x80) >> 7)
                    association.property_index.append(tmp & 0x7F)
            self.association_list.append(association)
        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def get_item_property_association(self) -> List[Association]:
        return self.association_list

    def print_box(self) -> None:
        super(ItemPropertyAssociation, self).print_box()
        print("entry_cout :", self.entry_cout)
        print("association_count :", len(self.association_list))

        for association in self.association_list:
            print("\titem_ID :", association.item_ID)
            print("\t\tessential      :", association.essential)
            print("\t\tproperty_index :", association.property_index)


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
