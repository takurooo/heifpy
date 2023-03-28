# -----------------------------------
# import
# -----------------------------------
from heifpy.file import BinaryFileReader

from .basebox import FullBox


# -----------------------------------
# define
# -----------------------------------

# -----------------------------------
# function
# -----------------------------------


# -----------------------------------
# class
# -----------------------------------
class ItemInfoExtension:
    def __init__(self, extension_type):
        pass


class ItemInfoEntry(FullBox):
    """
    ISO/IEC 14496-12
    Box Type: ‘infe’
    """

    def __init__(self):
        super(ItemInfoEntry, self).__init__()
        self.item_ID = None
        self.item_protection_index = None
        self.item_name = None
        self.item_type = ""
        self.item_uri_type = None
        self.content_type = None
        self.content_encoding = None
        self.extension_type = None
        self.iteminfoext = None

    def parse(self, reader: BinaryFileReader) -> None:
        super(ItemInfoEntry, self).parse(reader)

        if self.get_version() == 0 or self.get_version() == 1:
            self.item_ID = reader.read16()
            self.item_protection_index = reader.read16()
            self.item_name = reader.read_null_terminated()
            self.content_type = reader.read_null_terminated()
            if not self.read_complete(reader):
                self.content_encoding = reader.read_null_terminated()  # optional

            if self.get_version() == 1 and 0 < reader.num_bytes_left():
                self.extension_type = reader.read32()  # optional
                self.iteminfoext = ItemInfoExtension(self.extension_type)  # optional

        if self.get_version() >= 2:
            if self.get_version() == 2:
                self.item_ID = reader.read16()
            elif self.get_version() == 3:
                self.item_ID = reader.read32()

            self.item_protection_index = reader.read16()
            self.item_type = reader.read_str32()

            self.item_name = reader.read_null_terminated()

            if self.item_type == "mime":
                self.content_type = reader.read_null_terminated()
                if not self.read_complete(reader):
                    self.content_encoding = reader.read_null_terminated()  # optional
            elif self.item_type == "uri ":
                self.item_uri_type = reader.read_null_terminated()

    def print_box(self) -> None:
        super(ItemInfoEntry, self).print_box()
        print("item_ID               :", self.item_ID)
        print("item_protection_index :", self.item_protection_index)
        print("item_name             :", self.item_name)
        print("item_type             :", self.item_type)
        print("item_uri_type         :", self.item_uri_type)
        print("content_type          :", self.content_type)
        print("content_encoding      :", self.content_encoding)
        print("extension_type        :", self.extension_type)


# -----------------------------------
# main
# -----------------------------------
if __name__ == "__main__":
    pass
