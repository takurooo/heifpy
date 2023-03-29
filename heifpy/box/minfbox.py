from heifpy.binary import BinaryFileReader

from . import boxutils
from .basebox import Box
from .hmhdbox import HintMediaHeaderBox
from .smhdbox import SoundMediaHeaderBox
from .stblbox import SampleTableBox
from .vmhdbox import VideoMediaHeaderBox


class MediaInformationBox(Box):
    """
    ISO/IEC 14496-12
    Box	Type:   ‘minf’
    Container:   Media Box (‘mdia’)
    Mandatory:   Yes
    Quantity:   Exactly one
    """

    def __init__(self):
        super().__init__()
        self.vmhd = None
        self.smhd = None
        self.hmhd = None
        self.sthd = None
        self.nmhd = None
        self.dinf = None
        self.dref = None
        self.stbl = None

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        while not self.read_complete(reader):
            box_size, box_type = boxutils.read_box_header(reader)

            if box_type == "vmhd":
                self.vmhd = VideoMediaHeaderBox()
                self.vmhd.parse(reader)
            elif box_type == "smhd":
                self.smhd = SoundMediaHeaderBox()
                self.smhd.parse(reader)
            elif box_type == "hmhd":
                self.hmhd = HintMediaHeaderBox()
                self.hmhd.parse(reader)
            elif box_type == "sthd":
                reader.seek(box_size, 1)  # TODO sthd
            elif box_type == "nmhd":
                reader.seek(box_size, 1)  # TODO nmhd
            elif box_type == "dinf":
                reader.seek(box_size, 1)  # TODO dinf
            elif box_type == "dref":
                reader.seek(box_size, 1)  # TODO dref
            elif box_type == "stbl":
                self.stbl = SampleTableBox()
                self.stbl.parse(reader)
            else:
                reader.seek(box_size, 1)

        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        if self.vmhd is not None:
            self.vmhd.print_box()
        if self.smhd is not None:
            self.smhd.print_box()
        if self.hmhd is not None:
            self.hmhd.print_box()
        if self.stbl is not None:
            self.stbl.print_box()


if __name__ == "__main__":
    pass
