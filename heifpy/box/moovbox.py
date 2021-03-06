# -----------------------------------
# import
# -----------------------------------

from . import boxutils
from .basebox import Box
from .mvhdbox import MovieHeaderBox
from .trackbox import TrackBox
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
class MovieBox(Box):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘moov’
    Container:   File
    Mandatory:   Yes
    Quantity:   Exactly One
    """

    def __init__(self):
        super(MovieBox, self).__init__()
        self.mvhd = None
        self.trak = []

    def parse(self, reader: BinaryFileReader) -> None:
        super(MovieBox, self).parse(reader)
        while not self.read_complete(reader):
            box_size, box_type = boxutils.read_box_header(reader)
            if box_type == 'mvhd':
                self.mvhd = MovieHeaderBox()
                self.mvhd.parse(reader)
            elif box_type == 'trak':
                trak = TrackBox()
                trak.parse(reader)
                self.trak.append(trak)
            else:
                reader.seek(box_size, 1)

    def print_box(self) -> None:
        super(MovieBox, self).print_box()
        if self.mvhd is not None:
            self.mvhd.print_box()
        for trak in self.trak:
            trak.print_box()


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
