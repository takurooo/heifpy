from heifpy.binary import BinaryFileReader

from . import boxutils
from .basebox import Box, FullBox


class SampleEntry(Box):
    def __init__(self):
        super().__init__()
        self.data_reference_index = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        for _ in range(6):
            _ = reader.read8()  # reserved=0
        self.data_reference_index = reader.read16()

    def print_box(self) -> None:
        print("data_reference_index :", self.data_reference_index)


class AudioSampleEntry(SampleEntry):
    def __init__(self):
        super().__init__()
        self.channelcount = 0
        self.samplesize = 0
        self.pre_defined = 0
        self.samplerate = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        for _ in range(2):
            _ = reader.read32()  # reserved=0

        self.channelcount = reader.read16()
        self.samplesize = reader.read16()
        self.pre_defined = reader.read16()
        self.samplerate = reader.read32()

        self.to_box_end(reader)  # TODO

    def print_box(self) -> None:
        print("channelcount :", self.channelcount)
        print("samplesize   :", self.samplesize)
        print("samplerate   :", self.samplerate)


class SampleDescriptionBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘stsd’
    Container:   Sample Table Box (‘stbl’)
    Mandatory:   Yes
    Quantity:   Exactly one
    """

    def __init__(self):
        super().__init__()
        self.avc1 = None
        self.twos = None
        self.ipcm = None
        self.rtmd = None
        self.entry_count = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.entry_count = reader.read32()
        for _ in range(self.entry_count):
            box_size, box_type = boxutils.read_box_header(reader)
            # print(box_type)
            if box_type == "avc1":  # Advanced Video Coding
                reader.seek(box_size, 1)  # TODO avc1
            elif box_type == "twos":  # Uncompressed 16-bit audio
                self.twos = AudioSampleEntry()
                self.twos.parse(reader)
            elif box_type == "ipcm":
                self.ipcm = AudioSampleEntry()
                self.ipcm.parse(reader)
            # Real Time Metadata Sample Entry(XAVC Format)
            elif box_type == "rtmd":
                reader.seek(box_size, 1)  # TODO rtmd
            else:
                reader.seek(box_size, 1)

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        if self.avc1 is not None:
            self.avc1.print_box()
        if self.twos is not None:
            self.twos.print_box()
        if self.ipcm is not None:
            self.ipcm.print_box()
        if self.rtmd is not None:
            self.rtmd.print_box()


if __name__ == "__main__":
    pass
