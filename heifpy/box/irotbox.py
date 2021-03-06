# -----------------------------------
# import
# -----------------------------------
from .item_property import ItemProperty
from heifpy.file import BinaryFileReader


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------
class ItemRotation(ItemProperty):
    """
    ISO/IEC 23008-12
    Box Type: ‘irot’
    """

    def __init__(self):
        super(ItemRotation, self).__init__()
        self.angle = None

    def parse(self, reader: BinaryFileReader) -> None:
        super(ItemRotation, self).parse(reader)

        tmp = reader.read8()
        self.angle = tmp & 0x3
        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super(ItemRotation, self).print_box()
        print("angle :", self.angle)


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
