# -----------------------------------
# import
# -----------------------------------
from typing import List

from heifpy.file import BinaryFileReader

from . import boxutils
from .basebox import Box
from .colrbox import ColourInformationBox
from .hvccbox import HEVCConfigurationBox
from .irotbox import ItemRotation
from .ispebox import ImageSpatialExtentsProperty
from .item_property import ItemProperty
from .pixibox import PixelInformationProperty


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------


# -----------------------------------
# class
# -----------------------------------
class ItemPropertyContainerBox(Box):
    """
    ISO/IEC 23008-12
    Box Type: ‘ipco’
    """

    def __init__(self):
        super(ItemPropertyContainerBox, self).__init__()
        self.item_properties = []

    def parse(self, reader: BinaryFileReader) -> None:
        super(ItemPropertyContainerBox, self).parse(reader)

        self.item_properties = []
        while not self.read_complete(reader):
            box_size, box_type = boxutils.read_box_header(reader)

            item_property = None
            if box_type == "irot":
                item_property = ItemRotation()
            elif box_type == "colr":
                item_property = ColourInformationBox()
            elif box_type == "hvcC":
                item_property = HEVCConfigurationBox()
            elif box_type == "ispe":
                item_property = ImageSpatialExtentsProperty()
            elif box_type == "pixi":
                item_property = PixelInformationProperty()
            else:
                reader.seek(box_size, 1)

            if item_property is not None:
                item_property.parse(reader)
                self.item_properties.append(item_property)

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super(ItemPropertyContainerBox, self).print_box()
        for item_property in self.item_properties:
            item_property.print_box()

    def get_item_properties(self) -> List[ItemProperty]:
        return self.item_properties


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
