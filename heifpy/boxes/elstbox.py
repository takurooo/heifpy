from heifpy.binary import BinaryFileReader

from .basebox import FullBox


class EditListEntry:
    def __init__(self):
        self.segment_duration = 0
        self.media_time = 0
        self.media_rate_integer = 0
        self.media_rate_fraction = 0


class EditListBox(FullBox):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘elst’
    Container:   Movie Box (‘trak’)
    Mandatory:   No
    Quantity:   Zero or one
    """

    def __init__(self):
        super().__init__()
        self.entry_count = 0
        self.entries = []

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.entry_count = reader.read32()
        self.entries = []
        for _ in range(self.entry_count):
            elst_entry = EditListEntry()
            if self.get_version() == 1:
                elst_entry.segment_duration = reader.read64()
                elst_entry.media_time = reader.read64()
            else:
                elst_entry.segment_duration = reader.read32()
                elst_entry.media_time = reader.read32()

            elst_entry.media_rate_integer = reader.read16()
            elst_entry.media_rate_fraction = reader.read16()

            self.entries.append(elst_entry)

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()

        for i, entry in enumerate(self.entries):
            print(
                f"entry no.{i} segment_duration {entry.segment_duration} \
                media_time {entry.media_time} media_rate_integer {entry.media_rate_integer} \
                media_rate_fraction {entry.media_rate_fraction}"
            )


if __name__ == "__main__":
    pass
