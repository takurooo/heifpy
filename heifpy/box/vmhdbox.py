from heifpy.binary import BinaryFileReader

from .basebox import FullBox


class VideoMediaHeaderBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘vmhd’
    Container:   Media Information Box (‘minf’)
    Mandatory:   Yes
    Quantity:   Exactly one
    """

    def __init__(self):
        super().__init__()
        self.graphicsmode = 0
        self.opcolor = []

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.graphicsmode = reader.read16()  # copy = 0
        for _ in range(3):
            self.opcolor.append(reader.read16())  # {0,0,0}

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print("graphicmode :", self.graphicsmode)
        print("opcolor     :", self.opcolor)


if __name__ == "__main__":
    pass
