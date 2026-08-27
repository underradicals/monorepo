from os.path import join
from typing import LiteralString


class MetaPathsIO(type):
    pass


def make_path_property(project_name: str) -> property:
    return property(fget=lambda cls: join(cls.ROOT, project_name))


def create_attr(project_name: str):
    property_name = project_name.upper()
    setattr(MetaPathsIO, property_name, make_path_property(project_name))


class PathsIO(metaclass=MetaPathsIO):
    # Root Directories
    ROOT: LiteralString = "G:\\"
    MONOREPO_ROOT: LiteralString = join(ROOT, "Projects\\monorepo")
    ASSETS: LiteralString = join(ROOT, "Assets")
    DATA_ROOT: LiteralString = join(ASSETS, "Data")
    IMAGE_ROOT: LiteralString = join(ASSETS, "Images")

    # Project Directories
    D2_DATA: LiteralString = join(DATA_ROOT, "d2_data")

    # Raw Data From Sources
    D2_DATA_RAW_DATA: LiteralString = join(D2_DATA, "Raw")
    D2_DATA_CSV_DATA: LiteralString = join(D2_DATA_RAW_DATA, "Csv")
    D2_DATA_JSONL_DATA: LiteralString = join(D2_DATA_RAW_DATA, "Jsonl")

    # Data Ready for Pre Processing
    D2_DATA_BRONZE_DATA: LiteralString = join(D2_DATA, "Bronze")

    # Data Ready for Post Processing
    D2_DATA_SILVER_DATA: LiteralString = join(D2_DATA, "Silver")

    # Data Ready for Analysis
    D2_DATA_GOLD_DATA: LiteralString = join(D2_DATA, "Gold")

    @classmethod
    def create_dirs(cls):
        pass


def main():
    print("Paths_IO Package is Health...")
