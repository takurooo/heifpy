# -----------------------------------
# import
# -----------------------------------
from heifpy.file import BinaryFileReader

from .basebox import FullBox


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------


class TrackHeaderBox(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘tkhd’
    Container: Track Box('trak')
    Mandatory: Yes
    Quantity: Exactly one
    """

    def __init__(self):
        super(TrackHeaderBox, self).__init__()
        self.creation_time = 0
        self.modification_time = 0
        self.track_ID = 0
        self.duration = 0
        self.layer = 0
        self.alternate_group = 0
        self.volume = 0
        self.matrix = []
        self.width = 0
        self.height = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super(TrackHeaderBox, self).parse(reader)

        if self.get_version() == 1:
            self.creation_time = reader.read64()
            self.modification_time = reader.read64()
            self.track_ID = reader.read32()
            reader.read32()  # reserved
            self.duration = reader.read64()
        else:
            self.creation_time = reader.read32()
            self.modification_time = reader.read32()
            self.track_ID = reader.read32()
            reader.read32()  # reserved
            self.duration = reader.read32()

        reader.read32()  # reserved
        reader.read32()  # reserved

        self.layer = reader.read16()
        self.alternate_group = reader.read16()
        self.volume = reader.read16()

        reader.read16()  # reserved

        self.matrix = []
        for _ in range(9):
            self.matrix.append(reader.read32())

        self.width = reader.read32()
        self.height = reader.read32()

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super(TrackHeaderBox, self).print_box()
        print("creation_time     :", self.creation_time)
        print("modification_time :", self.modification_time)
        print("track_ID          :", self.track_ID)
        print("duration          :", self.duration)
        print("layer             :", self.layer)
        print("alternate_group   :", self.alternate_group)
        print("volume            :", self.volume)
        print("matrix            :", self.matrix)
        print("width             :", self.width >> 16)
        print("height            :", self.height >> 16)


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
