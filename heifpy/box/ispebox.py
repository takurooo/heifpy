from typing import Tuple

from heifpy.binary import BinaryFileReader

from .item_property import ItemFullProperty


class ImageSpatialExtentsProperty(ItemFullProperty):
    """
    ISO/IEC 23008-12
    Box Type: ‘ispe’
    """

    def __init__(self):
        super().__init__()
        self.image_width = 0
        self.image_height = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.image_width = reader.read32()
        self.image_height = reader.read32()
        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def get_image_width_height(self) -> Tuple[int, int]:
        return (self.image_width, self.image_height)

    def print_box(self) -> None:
        super().print_box()
        print("image_width  :", self.image_width)
        print("image_height :", self.image_height)


if __name__ == "__main__":
    pass
