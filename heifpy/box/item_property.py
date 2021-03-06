# -----------------------------------
# import
# -----------------------------------
from .basebox import Box, FullBox
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
class ItemProperty(Box):
    """
    ISO/IEC 23008-12
    """

    def __init__(self):
        super(ItemProperty, self).__init__()
        # self.skip_to_end(f)  # TODO

    def parse(self, reader: BinaryFileReader) -> None:
        super(ItemProperty, self).parse(reader)

    def print_box(self) -> None:
        super(ItemProperty, self).print_box()


class ItemFullProperty(FullBox):
    """
    ISO/IEC 23008-12
    """

    def __init__(self):
        super(ItemFullProperty, self).__init__()

    def parse(self, reader: BinaryFileReader) -> None:
        super(ItemFullProperty, self).parse(reader)

    def print_box(self) -> None:
        super(ItemFullProperty, self).print_box()


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
