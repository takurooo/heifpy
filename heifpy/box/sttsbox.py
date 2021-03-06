# -----------------------------------
# import
# -----------------------------------
from .basebox import FullBox
from heifpy.file import BinaryFileReader


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------
class DecodingTimeToSampleBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘stts’
    Container:   Sample Table Box (‘stbl’)
    Mandatory:   Yes
    Quantity:   Exactly one
    """

    def __init__(self):
        super(DecodingTimeToSampleBox, self).__init__()
        self.entry_count = 0
        self.sample_count = []
        self.sample_delta = []

    def parse(self, reader: BinaryFileReader) -> None:
        super(DecodingTimeToSampleBox, self).parse(reader)

        self.entry_count = reader.read32()

        for _ in range(self.entry_count):
            self.sample_count.append(reader.read32())
            self.sample_delta.append(reader.read32())

        assert self.read_complete(reader), f'{self.type} num bytes left not 0.'

    def print_box(self) -> None:
        super(DecodingTimeToSampleBox, self).print_box()
        print("entry_count   :", self.entry_count)
        print("sample_count  :", self.sample_count)
        print("sample_delta  :", self.sample_delta)


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
