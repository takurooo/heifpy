from heifpy.binary import BinaryFileReader

from . import boxutils
from .basebox import Box
from .edtsbox import EditBox
from .mdiabox import MediaBox
from .tkhdbox import TrackHeaderBox


class TrackBox(Box):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘trak’
    Container:   Movie Box (‘moov’)
    Mandatory:   Yes
    Quantity:   One or more
    """

    def __init__(self):
        super().__init__()
        self.tkhd = None
        self.tref = None
        self.edts = None
        self.mdia = None

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        while not self.read_complete(reader):
            box_size, box_type = boxutils.read_box_header(reader)

            if box_type == "tkhd":
                self.tkhd = TrackHeaderBox()
                self.tkhd.parse(reader)
            elif box_type == "edts":
                self.edts = EditBox()
                self.edts.parse(reader)
            elif box_type == "mdia":
                self.mdia = MediaBox()
                self.mdia.parse(reader)
            else:
                reader.seek(box_size, 1)

    def print_box(self) -> None:
        super().print_box()
        if self.tkhd is not None:
            self.tkhd.print_box()
        if self.edts is not None:
            self.edts.print_box()
        if self.mdia is not None:
            self.mdia.print_box()


if __name__ == "__main__":
    pass
