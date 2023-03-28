# -----------------------------------
# import
# -----------------------------------
from typing import Tuple

from heifpy.file import BinaryFileReader

from .item_property import ItemFullProperty


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------


# -----------------------------------
# class
# -----------------------------------
class ImageSpatialExtentsProperty(ItemFullProperty):
    """
    ISO/IEC 23008-12
    Box Type: ‘ispe’
    """

    def __init__(self):
        super(ImageSpatialExtentsProperty, self).__init__()
        self.image_width = 0
        self.image_height = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super(ImageSpatialExtentsProperty, self).parse(reader)

        self.image_width = reader.read32()
        self.image_height = reader.read32()
        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def get_image_width_height(self) -> Tuple[int, int]:
        return (self.image_width, self.image_height)

    def print_box(self) -> None:
        super(ImageSpatialExtentsProperty, self).print_box()
        print("image_width  :", self.image_width)
        print("image_height :", self.image_height)


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
