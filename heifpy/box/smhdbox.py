from heifpy.binary import BinaryFileReader

from .basebox import FullBox


class SoundMediaHeaderBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘smhd’
    Container:   Media Information Box (‘minf’)
    Mandatory:   Yes
    Quantity:   Exactly one specific media header shall be present
    """

    def __init__(self):
        super().__init__()
        self.balance = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.balance = reader.read16()  # balance = 0
        _ = reader.read16()  # reserved = 0

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print("balance :", self.balance)


if __name__ == "__main__":
    pass
