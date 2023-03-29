from heifpy.binary import BinaryFileReader

from .basebox import Box, FullBox


class ItemProperty(Box):
    """
    ISO/IEC 23008-12
    """

    def __init__(self):
        super().__init__()
        # self.skip_to_end(f)  # TODO

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

    def print_box(self) -> None:
        super().print_box()


class ItemFullProperty(FullBox):
    """
    ISO/IEC 23008-12
    """

    def __init__(self):
        super().__init__()

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

    def print_box(self) -> None:
        super().print_box()


if __name__ == "__main__":
    pass
