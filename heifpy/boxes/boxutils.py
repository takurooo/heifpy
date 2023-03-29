from typing import Tuple

from heifpy.binary import BinaryFileReader


def read_box_header(reader: BinaryFileReader) -> Tuple[int, str]:
    box_size = reader.read32()
    box_type = reader.read_str32()
    reader.seek(-8, 1)
    return (box_size, box_type)


if __name__ == "__main__":
    pass
