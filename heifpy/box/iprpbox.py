from heifpy.file import BinaryFileReader

from . import boxutils
from .basebox import Box
from .ipcobox import ItemPropertyContainerBox
from .ipmabox import ItemPropertyAssociation


# class SampleEntry(Box):
#
#     def __init__(self, f):
#         super(SampleEntry, self).__init__(f)
#         self.data_reference_index
#         self.parse(f)
#
#     def parse(self, f):
#         for _ in range(8):
#             _ = futils.read8(f, 'big')
#         self.data_reference_index  =futils.read16(f, 'big')
#
#     def print_box(self):
#         super(SampleEntry, self).print_box()
#         print("data_reference_index :",  self.data_reference_index)
#
# class VisualSampleEntry(SampleEntry):
#
#     def __init__(self, f):
#         super(VisualSampleEntry, self).__init__(f)
#
#     def parse(self, f):
#         pass
#
#     def print_box(self):
#         super(VisualSampleEntry, self).print_box()


class ItemPropertiesBox(Box):
    """
    ISO/IEC 23008-12
    Box Type: ‘iprp’
    Container: Meta box (‘meta’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self):
        super().__init__()
        # self.property_container = None
        self.ipco = None
        self.ipma = None

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        while not self.read_complete(reader):
            box_size, box_type = boxutils.read_box_header(reader)

            if box_type == "ipco":
                self.ipco = ItemPropertyContainerBox()
                self.ipco.parse(reader)
            elif box_type == "ipma":
                self.ipma = ItemPropertyAssociation()
                self.ipma.parse(reader)
            else:
                reader.seek(box_size, 1)

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        if self.ipco is not None:
            self.ipco.print_box()
        if self.ipma is not None:
            self.ipma.print_box()


if __name__ == "__main__":
    pass
