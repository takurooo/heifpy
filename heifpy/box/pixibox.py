# -----------------------------------
# import
# -----------------------------------
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
class PixelInformationProperty(ItemFullProperty):
    """
    ISO/IEC 23008-12
    Box Type: ‘pixi’
    """

    def __init__(self):
        super(PixelInformationProperty, self).__init__()
        self.num_channels = 0
        self.bits_per_channel = []

    def parse(self, reader: BinaryFileReader) -> None:
        super(PixelInformationProperty, self).parse(reader)
        self.num_channels = reader.read8()
        for i in range(self.num_channels):
            self.bits_per_channel.append(reader.read8())
        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super(PixelInformationProperty, self).print_box()
        print("image_width  :", self.num_channels)
        print("image_height :", self.bits_per_channel)


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
