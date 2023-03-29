from heifpy.binary import BinaryFileReader

from .basebox import Box


class NalArray:
    def __init__(self):
        self.array_completeness = 0
        self.NAL_unit_type = 0
        self.numNalus = 0
        self.nal_list = []


class HEVCDecoderConfigurationRecord:
    """
    ISO/IEC 14496-15
    """

    def __init__(self, reader: BinaryFileReader):
        self.configurationVersion = 0
        self.genera_profile_space = 0
        self.general_tier_flag = 0
        self.general_profile_idc = 0
        self.general_profile_compatibility_flags = 0
        self.general_constraint_indicator_flags = 0
        self.general_level_idc = 0
        self.min_spatial_segmentation_idc = 0
        self.parallelismType = 0
        self.chroma_format_idc = 0
        self.bit_depth_luma_minus8 = 0
        self.bit_depth_chroma_minus8 = 0
        self.avgFrameRate = 0
        self.constantFrameRate = 0
        self.numTemporalLayers = 0
        self.temporalIdNested = 0
        self.lengthSizeMinus = 0
        # self.numOfArrays = None
        # self.nalUnits = None
        # self.array_completeness = None
        # self.NAL_unit_type = None
        # self.numNalus = None
        # self.nalUnitLength = None
        self.nal_array = []
        self.parse(reader)

    def parse(self, reader: BinaryFileReader) -> None:
        self.configurationVersion = reader.read8()
        tmp = reader.read8()
        self.genera_profile_space = (tmp & 0xC0) >> 6
        self.general_tier_flag = (tmp & 0x20) >> 5
        self.general_profile_idc = tmp & 0x1F
        self.general_profile_compatibility_flags = reader.read32()
        self.general_constraint_indicator_flags = (
            (reader.read8() << 40)
            | (reader.read8() << 32)
            | (reader.read8() << 24)
            | (reader.read8() << 16)
            | (reader.read8() << 8)
            | (reader.read8() << 0)
        )
        self.general_level_idc = reader.read8()

        self.min_spatial_segmentation_idc = reader.read16() & 0x0FFF
        self.parallelismType = reader.read8() & 0b00000011
        self.chroma_format_idc = reader.read8() & 0b00000011
        self.bit_depth_luma_minus8 = reader.read8() & 0b00000111
        self.bit_depth_chroma_minus8 = reader.read8() & 0b00000111
        self.avgFrameRate = reader.read16()

        tmp = reader.read8()
        self.constantFrameRate = (tmp & 0b11000000) >> 6
        self.numTemporalLayers = (tmp & 0b00111000) >> 3
        self.temporalIdNested = (tmp & 0b00000100) >> 2
        self.lengthSizeMinus = tmp & 0b00000011
        numOfArrays = reader.read8()

        for _ in range(numOfArrays):
            tmp = reader.read8()
            nal_array = NalArray()
            nal_array.array_completeness = (tmp & 0b10000000) >> 7
            nal_array.NAL_unit_type = tmp & 0b00111111
            nal_array.numNalus = reader.read16()

            nal_unit = b""
            for _ in range(nal_array.numNalus):
                nalUnitLength = reader.read16()
                for _ in range(nalUnitLength):
                    nal_unit += reader.read_raw(1)
                nal_array.nal_list.append(nal_unit)

            self.nal_array.append(nal_array)


class HEVCConfigurationBox(Box):
    """
    ISO/IEC 14496-15
    for hvcC
    """

    def __init__(self):
        super().__init__()
        self.HEVCConfig = None

    def parse(self, reader: BinaryFileReader) -> None:
        super().parse(reader)

        self.HEVCConfig = HEVCDecoderConfigurationRecord(reader)
        assert self.read_complete(reader), f"{self.type} num bytes left not 0."

    def print_box(self) -> None:
        super().print_box()
        print(
            "configurationVersion                : ",
            self.HEVCConfig.configurationVersion,
        )
        print(
            "genera_profile_space                : ",
            self.HEVCConfig.genera_profile_space,
        )
        print(
            "general_tier_flag                   : ", self.HEVCConfig.general_tier_flag
        )
        print(
            "general_profile_idc                 : ",
            self.HEVCConfig.general_profile_idc,
        )
        print(
            f"general_profile_compatibility_flags : \
                {self.HEVCConfig.general_profile_compatibility_flags:#x}"
        )
        print(
            f"general_constraint_indicator_flags  : \
                {self.HEVCConfig.general_constraint_indicator_flags:#x}"
        )
        print(
            "general_level_idc                   : ", self.HEVCConfig.general_level_idc
        )
        print(
            "min_spatial_segmentation_idc        : ",
            self.HEVCConfig.min_spatial_segmentation_idc,
        )
        print("parallelismType                     : ", self.HEVCConfig.parallelismType)
        print(
            "chroma_format_idc                   : ", self.HEVCConfig.chroma_format_idc
        )
        print(
            "bit_depth_luma_minus8               : ",
            self.HEVCConfig.bit_depth_luma_minus8,
        )
        print(
            "bit_depth_chroma_minus8             : ",
            self.HEVCConfig.bit_depth_chroma_minus8,
        )
        print("avgFrameRate                        : ", self.HEVCConfig.avgFrameRate)
        print(
            "constantFrameRate                   : ", self.HEVCConfig.constantFrameRate
        )
        print(
            "numTemporalLayers                   : ", self.HEVCConfig.numTemporalLayers
        )
        print(
            "temporalIdNested                    : ", self.HEVCConfig.temporalIdNested
        )
        print("lengthSizeMinus                     : ", self.HEVCConfig.lengthSizeMinus)
        print("nalUnits")
        for nal_array in self.HEVCConfig.nal_array:
            print("\tarray_completeness : ", nal_array.array_completeness)
            print("\tNAL_unit_type      : ", nal_array.NAL_unit_type)
            for nalUnit in nal_array.nal_list:
                print("\t\tnalUnit : ", nalUnit)


if __name__ == "__main__":
    pass
