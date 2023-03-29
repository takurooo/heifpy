from typing import List

from heifpy.file import BinaryFileReader

from .basebox import Box


class FileTypeBox(Box):
    """
    ISO/IEC 14496-12
    Box Type: `ftyp’
    Container: File
    Mandatory: Yes
    Quantity: Exactly one
    """

    def __init__(self):
        super().__init__()
        self.major_brand = ""
        self.minor_version = 0
        self.compatible_brands = []

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)
        self.major_brand = reader.read_str32()
        self.minor_version = reader.read32()

        self.compatible_brands = []
        while not self.read_complete(reader):
            self.compatible_brands.append(reader.read_str32())

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def get_major_brand(self) -> str:
        return self.major_brand

    def get_minor_version(self) -> int:
        return self.minor_version

    def get_compatible_brands(self) -> List[str]:
        return self.compatible_brands

    def print_box(self) -> None:
        super().print_box()
        print("major_brand       :", self.major_brand)
        print("minor_version     :", self.minor_version)
        print("compatible_brands :", self.compatible_brands)


if __name__ == "__main__":
    pass
