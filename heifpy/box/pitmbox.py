from heifpy.binary import BinaryFileReader

from .basebox import FullBox


class PrimaryItemBox(FullBox):
    """
    Box Type: ‘pitm’
    Container: Meta box (‘meta’)
    Mandatory: No
    Quantity: Zero or one
    """

    def __init__(self):
        super().__init__()
        self.item_ID = 0

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.item_ID = reader.read16()
        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def get_primary_item_id(self) -> int:
        return self.item_ID

    def print_box(self) -> None:
        super().print_box()
        print("item_ID :", self.item_ID)


if __name__ == "__main__":
    pass
