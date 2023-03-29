import os
import struct


__all__ = ["BinaryFileReader"]

BIG_LITTLE = {"little": "<", "big": ">"}


class BinaryFileReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.f = open(file_path, "rb")
        self.file_size = os.path.getsize(file_path)

        self.start_fp = self.f.tell()

        self.num_bits_left = 0
        self.bit_buffer = 0

        self.byteorder = "big"

    def set_byteorder(self, byteorder: str) -> None:
        self.byteorder = byteorder

    def close(self) -> None:
        if self.f:
            self.f.close()

    def num_bytes_left(self) -> int:
        return self.file_size - (self.f.tell() - self.start_fp)

    def seek_to_end(self) -> None:
        self.seek(self.file_size)

    def seek(self, offset: int, whence: int = 0) -> None:
        self.f.seek(offset, whence)

    def tell(self) -> int:
        return self.f.tell()

    def read_raw(self, size: int) -> bytes:
        return self.f.read(size)

    def read_str8(self) -> str:
        return self.f.read(1).decode()

    def read_str16(self) -> str:
        s = self.f.read(2).decode()
        if self.byteorder == "little":
            s = s[::-1]
        return s

    def read_str24(self) -> str:
        filler = 0
        filler = filler.to_bytes(1, byteorder="big", signed=True)
        a = self.f.read(1)
        b = self.f.read(1)
        c = self.f.read(1)
        if self.byteorder == "big":
            bin24 = a + b + c
        elif self.byteorder == "little":
            bin24 = c + b + a
        else:
            raise ValueError(f"Invalid byteorder {self.byteorder}")

        return bin24.decode()

    def read_str32(self) -> str:
        s = self.f.read(4).decode()
        if self.byteorder == "little":
            s = s[::-1]
        return s

    def read_str64(self) -> str:
        s = self.f.read(8).decode()
        if self.byteorder == "little":
            s = s[::-1]
        return s

    def read8(self, signed: bool = False) -> int:
        if signed:
            format_char = "b"
        else:
            format_char = "B"
        return struct.unpack(BIG_LITTLE[self.byteorder] + format_char, self.f.read(1))[
            0
        ]

    def read16(self, signed: bool = False) -> int:
        if signed:
            format_char = "h"
        else:
            format_char = "H"
        return struct.unpack(BIG_LITTLE[self.byteorder] + format_char, self.f.read(2))[
            0
        ]

    def read24(self, signed: bool = False) -> int:
        filler = 0
        filler = filler.to_bytes(1, byteorder="big", signed=True)
        a = self.f.read(1)
        b = self.f.read(1)
        c = self.f.read(1)
        if self.byteorder == "big":
            bin24 = a + b + c
        elif self.byteorder == "little":
            bin24 = c + b + a
        else:
            raise ValueError(f"Invalid byteorder {self.byteorder}")

        bin32 = bin24 + filler  # to 32bit
        if signed:
            format_char = "l"
        else:
            format_char = "L"
        ret24 = struct.unpack(BIG_LITTLE[self.byteorder] + format_char, bin32)[0] >> 8
        return ret24

    def read32(self, signed: bool = False) -> int:
        if signed:
            format_char = "l"
        else:
            format_char = "L"
        return struct.unpack(BIG_LITTLE[self.byteorder] + format_char, self.f.read(4))[
            0
        ]

    def read64(self, signed: bool = False) -> int:
        if signed:
            format_char = "q"
        else:
            format_char = "Q"
        return struct.unpack(BIG_LITTLE[self.byteorder] + format_char, self.f.read(8))[
            0
        ]

    def readn(self, size_bits: int, signed: bool = False) -> int:
        if size_bits == 0:
            return 0

        if size_bits == 64:
            data = self.read64(signed)
        elif size_bits == 32:
            data = self.read32(signed)
        elif size_bits == 24:
            data = self.read24(signed)
        elif size_bits == 16:
            data = self.read16(signed)
        elif size_bits == 8:
            data = self.read8(signed)
        else:
            raise ValueError()

        return data

    def is_byte_aligned(self) -> bool:
        return self.num_bits_left == 0

    def readbits(self, num_bits: int) -> int:
        # big endian only

        if num_bits == 0:
            return 0

        if num_bits > 8:
            return_bits = self.read8() << (num_bits - 8)
            return_bits |= self.readbits(num_bits - 8)
            return return_bits

        if self.num_bits_left >= num_bits:
            return_bits = self.bit_buffer >> (8 - num_bits)
            self.bit_buffer = (self.bit_buffer << num_bits) & 0xFF
            self.num_bits_left -= num_bits

        else:
            read_bits = self.read8()
            self.bit_buffer = (self.bit_buffer << self.num_bits_left) | read_bits
            self.num_bits_left += 8
            return_bits = self.bit_buffer >> (self.num_bits_left - num_bits)
            self.bit_buffer = (
                self.bit_buffer << (8 - (self.num_bits_left - num_bits))
            ) & 0xFF
            self.num_bits_left -= num_bits

        return return_bits

    def read_null_terminated(self) -> str:
        null = b"\x00"
        s = ""
        while True:
            c = self.read_str8()
            s += c
            if c.encode() == null:
                break
        return s


if __name__ == "__main__":
    pass
