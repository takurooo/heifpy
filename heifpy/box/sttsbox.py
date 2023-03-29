from heifpy.binary import BinaryFileReader

from .basebox import FullBox


class DecodingTimeToSampleBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘stts’
    Container:   Sample Table Box (‘stbl’)
    Mandatory:   Yes
    Quantity:   Exactly one
    """

    def __init__(self):
        super().__init__()
        self.entry_count = 0
        self.sample_count = []
        self.sample_delta = []

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.entry_count = reader.read32()

        for _ in range(self.entry_count):
            self.sample_count.append(reader.read32())
            self.sample_delta.append(reader.read32())

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print("entry_count   :", self.entry_count)
        print("sample_count  :", self.sample_count)
        print("sample_delta  :", self.sample_delta)


if __name__ == "__main__":
    pass
