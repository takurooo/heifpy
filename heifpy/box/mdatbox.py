from heifpy.file import BinaryFileReader

from .basebox import Box


class MediaDataBox(Box):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘mdat’
    Container:   File
    Mandatory:   No
    Quantity:   Zero	or	more
    """

    def __init__(self):
        super().__init__()

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)
        self.to_box_end(reader)

    def print_box(self) -> None:
        super().print_box()


if __name__ == "__main__":
    pass
