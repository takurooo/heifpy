# -----------------------------------
# import
# -----------------------------------
import struct


__all__ = ["BinaryFileWriter"]
# -----------------------------------
# define
# -----------------------------------
BIG_LITTLE = {"little": "<", "big": ">"}


# -----------------------------------
# function
# -----------------------------------


class BinaryFileWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.f = open(file_path, "wb")
        self.byteorder = "big"

    def set_byteorder(self, byteorder: str) -> None:
        self.byteorder = byteorder

    def close(self) -> None:
        if self.f:
            self.f.close()

    def seek(self, offset: int, whence: int = 0) -> None:
        self.f.seek(offset, whence)

    def tell(self) -> int:
        return self.f.tell()

    def write8(self, v: int) -> None:
        self.f.write(struct.pack(BIG_LITTLE[self.byteorder] + "B", v))

    def write16(self, v: int) -> None:
        self.f.write(struct.pack(BIG_LITTLE[self.byteorder] + "H", v))

    def write24(self, v: int) -> None:
        b = []
        if self.byteorder == "big":
            c = (v >> 16) & 0xFF
            self.write8(c)
            c = (v >> 8) & 0xFF
            self.write8(c)
            c = (v >> 0) & 0xFF
            self.write8(c)
        else:
            c = (v >> 0) & 0xFF
            self.write8(c)
            c = (v >> 8) & 0xFF
            self.write8(c)
            c = (v >> 16) & 0xFF
            self.write8(c)

    def write32(self, v: int) -> None:
        self.f.write(struct.pack(BIG_LITTLE[self.byteorder] + "L", v))

    def write64(self, v: int) -> None:
        self.f.write(struct.pack(BIG_LITTLE[self.byteorder] + "Q", v))

    def write_str(self, v: str) -> None:
        self.f.write(v.encode("utf-8"))


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
