from heifpy.binary import BinaryFileReader

from .basebox import FullBox


class MediaHeaderBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘mdhd’
    Container:   Media Box (‘mdia’)
    Mandatory:   Yes
    Quantity:   Exactly One
    """

    def __init__(self):
        super().__init__()
        self.creation_time = 0
        self.modification_time = 0
        self.timescale = 0
        self.duration = 0
        self.pad = 0
        self.language = []
        self.pre_defined = 0

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

        self.pad = reader.readbits(1)
        for _ in range(3):
            self.language.append(reader.readbits(5))
        self.pre_defined = reader.read16()

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print("creation_time     :", self.creation_time)
        print("modification_time :", self.modification_time)
        print("timescale         :", self.timescale)
        print("duration          :", self.duration)
        print("pad               :", self.pad)
        print("language          :", self.language)
        print("pre_defined       :", self.pre_defined)


if __name__ == "__main__":
    pass
