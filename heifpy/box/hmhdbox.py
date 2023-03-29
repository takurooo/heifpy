from heifpy.binary import BinaryFileReader

from .basebox import FullBox


class HintMediaHeaderBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘hmhd’
    Container:   Media Information Box (‘minf’)
    Mandatory:   Yes
    Quantity:   Exactly one specific media header shall be present
    """

    def __init__(self):
        super().__init__()
        self.maxPDUsize = 0
        self.avgPDUsize = 0
        self.maxbitrate = 0
        self.avgbitrate = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.maxPDUsize = reader.read16()
        self.avgPDUsize = reader.read16()
        self.maxbitrate = reader.read16()
        self.avgbitrate = reader.read16()
        _ = reader.read32()  # reserved = 0

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print("maxPDUsize :", self.maxPDUsize)
        print("avgPDUsize :", self.avgPDUsize)
        print("maxbitrate :", self.maxbitrate)
        print("avgbitrate :", self.avgbitrate)


if __name__ == "__main__":
    pass
