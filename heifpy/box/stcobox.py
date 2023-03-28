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
class ChunkOffsetBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘stco’
    Container:   Sample Table Box (‘stbl’)
    Mandatory:   Yes
    Quantity:   Exactly One variant must be present
    """

    def __init__(self):
        super(ChunkOffsetBox, self).__init__()
        self.entry_count = 0
        self.chunk_offset = []

    def parse(self, reader: BinaryFileReader) -> None:
        super(ChunkOffsetBox, self).parse(reader)

        self.entry_count = reader.read32()

        if self.get_type() == "stco":
            for i in range(self.entry_count):
                self.chunk_offset.append(reader.read32())
        else:
            # co64
            for i in range(self.entry_count):
                self.chunk_offset.append(reader.read64())

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super(ChunkOffsetBox, self).print_box()
        print("entry_count  :", self.entry_count)
        print("chunk_offset :", self.chunk_offset)


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
