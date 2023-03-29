from heifpy.binary import BinaryFileReader

from .basebox import FullBox


class CompositionTimeToSample(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘ctts’
    Container:   Sample Table Box (‘stbl’)
    Mandatory:   Yes
    Quantity:   Zero or one
    """

    def __init__(self):
        super().__init__()
        self.entry_count = None
        self.sample_count = []
        self.sample_offset = []

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.entry_count = reader.read32()

        if self.get_version() == 0:
            for _ in range(self.entry_count):
                self.sample_count.append(reader.read32())
                self.sample_offset.append(reader.read32())
        elif self.get_version() == 1:
            for _ in range(self.entry_count):
                self.sample_count.append(reader.read32())
                self.sample_offset.append(reader.read32(signed=True))

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print("entry_count   :", self.entry_count)
        print("sample_count  :", self.sample_count)
        print("sample_offset :", self.sample_offset)


if __name__ == "__main__":
    pass
