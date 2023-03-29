from heifpy.file import BinaryFileReader

from .basebox import FullBox


class ChunkOffsetBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘stco’
    Container:   Sample Table Box (‘stbl’)
    Mandatory:   Yes
    Quantity:   Exactly One variant must be present
    """

    def __init__(self):
        super().__init__()
        self.entry_count = 0
        self.chunk_offset = []

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.entry_count = reader.read32()

        if self.get_type() == "stco":
            for _ in range(self.entry_count):
                self.chunk_offset.append(reader.read32())
        else:
            # co64
            for _ in range(self.entry_count):
                self.chunk_offset.append(reader.read64())

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print("entry_count  :", self.entry_count)
        print("chunk_offset :", self.chunk_offset)


if __name__ == "__main__":
    pass
