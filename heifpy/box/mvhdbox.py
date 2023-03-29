from heifpy.file import BinaryFileReader

from .basebox import FullBox


class MovieHeaderBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘mvhd’
    Container:   Movie Box (‘moov’)
    Mandatory:   Yes
    Quantity:   Exactly One
    """

    def __init__(self):
        super().__init__()
        self.creation_time = 0
        self.modification_time = 0
        self.timescale = 0
        self.duration = 0
        self.rate = 0
        self.volume = 0
        self.matrix = 0
        self.predefined = 0
        self.next_track_ID = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        if self.get_version() == 1:
            self.creation_time = reader.read64()
            self.modification_time = reader.read64()
            self.timescale = reader.read32()
            self.duration = reader.read64()
        else:
            self.creation_time = reader.read32()
            self.modification_time = reader.read32()
            self.timescale = reader.read32()
            self.duration = reader.read32()

        self.rate = reader.read32()
        self.volume = reader.read16()

        reader.read16()  # reserved
        reader.read32()  # reserved
        reader.read32()  # reserved

        self.matrix = []
        for _ in range(9):
            self.matrix.append(reader.read32())

        self.predefined = []
        for _ in range(6):
            self.predefined.append(reader.read32())

        self.next_track_ID = reader.read32()

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print("creation_time :", self.creation_time)
        print("modification_time :", self.modification_time)
        print("timescale :", self.timescale)
        print("duration :", self.duration)
        print("rate :", self.rate)
        print("volume :", self.volume)
        print("matrix :", self.matrix)
        print("predefined :", self.predefined)
        print("next_track_ID :", self.next_track_ID)


if __name__ == "__main__":
    pass
