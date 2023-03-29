from heifpy.binary import BinaryFileReader

from . import boxutils
from .basebox import FullBox
from .hdlrbox import HandlerReferenceBox
from .iinfbox import ItemInformationBox
from .ilocbox import ItemLocationBox
from .iprpbox import ItemPropertiesBox
from .irefbox import ItemReferenceBox
from .pitmbox import PrimaryItemBox


class MetaBox(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘meta’
    Container: File, Movie Box (‘moov’), or Track Box (‘trak’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self):
        super().__init__()
        self.hdlr = None
        self.pitm = None
        self.iinf = None
        self.iprp = None
        self.iref = None
        self.iloc = None

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        while not self.read_complete(reader):
            box_size, box_type = boxutils.read_box_header(reader)
            # print(box_type)
            if box_type == "hdlr":
                self.hdlr = HandlerReferenceBox()
                self.hdlr.parse(reader)
            elif box_type == "pitm":
                self.pitm = PrimaryItemBox()
                self.pitm.parse(reader)
            elif box_type == "iinf":
                self.iinf = ItemInformationBox()
                self.iinf.parse(reader)
            elif box_type == "iprp":
                self.iprp = ItemPropertiesBox()
                self.iprp.parse(reader)
            elif box_type == "iref":
                self.iref = ItemReferenceBox()
                self.iref.parse(reader)
            elif box_type == "iloc":
                self.iloc = ItemLocationBox()
                self.iloc.parse(reader)
            else:
                reader.seek(box_size, 1)

    def print_box(self) -> None:
        super().print_box()

        if self.hdlr is not None:
            self.hdlr.print_box()
        if self.pitm is not None:
            self.pitm.print_box()
        if self.iinf is not None:
            self.iinf.print_box()
        if self.iprp is not None:
            self.iprp.print_box()
        if self.iref is not None:
            self.iref.print_box()
        if self.iloc is not None:
            self.iloc.print_box()


if __name__ == "__main__":
    pass
