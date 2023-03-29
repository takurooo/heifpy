from heifpy.binary import BinaryFileReader

from . import boxutils
from .basebox import Box
from .elstbox import EditListBox


class EditBox(Box):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘edts’
    Container:   Track Box (‘trak’)
    Mandatory:   No
    Quantity:   Zero or one
    """

    def __init__(self):
        super().__init__()
        self.elst = None

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        while not self.read_complete(reader):
            box_size, box_type = boxutils.read_box_header(reader)

            if box_type == "elst":
                self.elst = EditListBox()
                self.elst.parse(reader)
            else:
                reader.seek(box_size, 1)

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        if self.elst is not None:
            self.elst.print_box()


if __name__ == "__main__":
    pass
