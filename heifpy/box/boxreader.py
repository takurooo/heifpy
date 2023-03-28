# -----------------------------------
# import
# -----------------------------------
from enum import Enum

from heifpy.file import BinaryFileReader

from . import boxutils
from .ftypebox import FileTypeBox
from .mdatbox import MediaDataBox
from .metabox import MetaBox


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------


class BoxReader:
    def __init__(self):
        self.ftyp = None
        self.meta = None
        self.mdat = None

    def read_boxes(self, reader: BinaryFileReader) -> None:
        while reader.num_bytes_left():
            box_size, box_type = boxutils.read_box_header(reader)
            # print(box_type)

            if box_type == "ftyp":
                self.ftyp = FileTypeBox()
                self.ftyp.parse(reader)
            elif box_type == "meta":
                self.meta = MetaBox()
                self.meta.parse(reader)
            elif box_type == "mdat":
                self.mdat = MediaDataBox()
                self.mdat.parse(reader)
            else:
                reader.seek(box_size, 1)

    def print_boxes(self) -> None:
        if self.ftyp is not None:
            self.ftyp.print_box()
        if self.meta is not None:
            self.meta.print_box()


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
