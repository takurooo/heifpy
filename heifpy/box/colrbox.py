# -----------------------------------
# import
# -----------------------------------
from heifpy.file import BinaryFileReader

from .basebox import Box


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------


class ColourInformationBox(Box):
    """
    ISO/IEC 14496-12
    Box Type: ‘colr’
    """

    def __init__(self):
        super(ColourInformationBox, self).__init__()
        self.colour_type = None
        self.colour_primaries = None
        self.transfer_characteristics = None
        self.matrix_coefficients = None
        self.full_range_flag = None

    def parse(self, reader: BinaryFileReader) -> None:
        super(ColourInformationBox, self).parse(reader)

        self.colour_type = reader.read_str32()
        if self.colour_type == "nclx":
            self.colour_primaries = reader.read16()
            self.transfer_characteristics = reader.read16()
            self.matrix_coefficients = reader.read16()
            tmp = reader.read8()
            self.full_range_flag = (tmp & 0x80) >> 7
        elif self.colour_type == "rICC":
            assert 0, f"not support {self.colour_type}"  # TODO
        elif self.colour_type == "prof":
            assert 0, f"not support {self.colour_type}"  # TODO

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super(ColourInformationBox, self).print_box()
        print("colour_type :", self.colour_type)
        print("colour_primaries :", self.colour_primaries)
        print("transfer_characteristics :", self.transfer_characteristics)
        print("matrix_coefficients :", self.matrix_coefficients)
        print("full_range_flag :", self.full_range_flag)


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
