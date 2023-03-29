from heifpy.file import BinaryFileReader


class Box:
    """
    ISO/IEC 14496-12
    """

    def __init__(self):
        self.start_pos = 0
        self.size = 0
        self.type = ""
        self.largesize = 0
        self.usertype = []

    def parse(self, reader: BinaryFileReader) -> None:
        self.start_pos = reader.tell()
        # size is an integer that specifies the number of bytes in this box,
        # including all its fields and contained boxes;
        # if size is 1 then the actual size is in the field large size;
        # if size is 0, then this box is the last one in the file,
        # and its contents extend to the end of the file (normally only used for a Media Data Box)
        self.size = reader.read32()
        # type identifies the box type;
        # standard boxes use a compact type, which is normally four printable characters,
        # to permit ease of identification, and is shown so in the boxes below.
        # User extensions use an extended type; in this case, the type field is set to ‘uuid’.
        self.type = reader.read_str32()

        if self.size == 1:
            self.largesize = reader.read64()
        elif self.size == 0:
            # box extends to end of file
            pass
        if self.type == "uuid":
            self.usertype = [reader.read8() for _ in range(16)]

    def get_size(self) -> int:
        if self.size == 1:
            return self.largesize
        return self.size

    def get_type(self) -> str:
        return self.type

    def get_start_pos(self) -> int:
        return self.start_pos

    def read_complete(self, reader: BinaryFileReader) -> bool:
        read_size = reader.tell() - self.start_pos
        return self.get_size() <= read_size

    def to_box_end(self, reader: BinaryFileReader) -> None:
        reader.seek(self.start_pos + self.get_size())

    def print_box(self) -> None:
        print()
        print("--------------------------")
        print(" boxtype   :", self.type)
        print(" boxsize   :", hex(self.size))
        print(" largesize :", self.largesize)
        print(" usertype  :", self.usertype)
        print(" filepos   :", hex(self.start_pos))
        print("--------------------------")


class FullBox(Box):
    def __init__(self):
        super().__init__()
        self.is_fullbox = True
        self.version = 0
        self.flags = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)
        # v_flags = bitstream.read32('big')
        # self.version = (v_flags & 0xff000000) >> 24
        # self.flags = (v_flags & 0x00ffffff)
        self.version = reader.readbits(8)
        self.flags = reader.readbits(24)

    def get_version(self) -> int:
        return self.version

    def get_flags(self) -> int:
        return self.flags

    def print_box(self) -> None:
        super().print_box()
        print("version :", self.version)
        print("flags   :", self.flags)


if __name__ == "__main__":
    pass
