# -----------------------------------
# import
# -----------------------------------
from .basebox import FullBox
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


class HandlerReferenceBox(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘hdlr’
    Container: Media Box (‘mdia’) or Meta Box (‘meta’)
    Mandatory: Yes
    Quantity: Exactly one
    """

    def __init__(self):
        super(HandlerReferenceBox, self).__init__()
        self.pre_defined = 0
        self.handler_type = ""
        self.name = ""

    def parse(self, reader: BinaryFileReader) -> None:
        super(HandlerReferenceBox, self).parse(reader)

        self.pre_defined = reader.read32()
        self.handler_type = reader.read_str32()
        for _ in range(3):
            _ = reader.read32()  # reserved

        self.name = ""
        if not self.read_complete(reader):
            self.name = reader.read_null_terminated()
            pass

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super(HandlerReferenceBox, self).print_box()
        print("pre_defined  :", self.pre_defined)
        print("handler_type :", self.handler_type)
        print("name         :", self.name)


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
