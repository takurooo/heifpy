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
class SampleSizeBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘stsz’
    Container:   Sample Table Box (‘stbl’)
    Mandatory:   Yes
    Quantity:   Exactly One variant must be present
    """

    def __init__(self):
        super(SampleSizeBox, self).__init__()
        self.sample_size = 0
        self.sample_count = 0
        self.entry_size = []

    def parse(self, reader: BinaryFileReader) -> None:
        super(SampleSizeBox, self).parse(reader)

        self.sample_size = reader.read32()
        self.sample_count = reader.read32()

        if self.sample_size == 0:
            for i in range(self.sample_count):
                self.entry_size.append(reader.read32())

        assert self.read_complete(reader), f'{self.type} num bytes left not 0.'

    def get_sample_size(self, idx: int) -> int:
        if self.sample_size == 0:
            return self.entry_size[idx]
        else:
            return self.sample_size

    def print_box(self) -> None:
        super(SampleSizeBox, self).print_box()
        print("sample_size  :", self.sample_size)
        print("sample_count :", self.sample_count)
        print("entry_size   :", self.entry_size)


# -----------------------------------
# main
# -----------------------------------
if __name__ == '__main__':
    pass
