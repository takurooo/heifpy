# -----------------------------------
# import
# -----------------------------------
from . import boxutils
from .basebox import Box
from .hdlrbox import HandlerReferenceBox
from .mdhdbox import MediaHeaderBox
from .minfbox import MediaInformationBox
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


class MediaBox(Box):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘mdia’
    Container:   Track Box (‘trak’)
    Mandatory:   Yes
    Quantity:   Exactly one
    """

    def __init__(self):
        super(MediaBox, self).__init__()
        self.mdhd = None
        self.hdlr = None
        self.minf = None

    def parse(self, reader: BinaryFileReader) -> None:
        super(MediaBox, self).parse(reader)

        while not self.read_complete(reader):
            box_size, box_type = boxutils.read_box_header(reader)
            if box_type == 'mdhd':
                self.mdhd = MediaHeaderBox()
                self.mdhd.parse(reader)
            elif box_type == 'hdlr':
                self.hdlr = HandlerReferenceBox()
                self.hdlr.parse(reader)
            elif box_type == 'minf':
                self.minf = MediaInformationBox()
                self.minf.parse(reader)
            else:
                reader.seek(box_size, 1)

        assert self.read_complete(reader), f'{self.type} num bytes left not 0.'

    def print_box(self) -> None:
        super(MediaBox, self).print_box()
        if self.mdhd is not None:
            self.mdhd.print_box()
        if self.hdlr is not None:
            self.hdlr.print_box()
        if self.minf is not None:
            self.minf.print_box()


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
