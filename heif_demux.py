import argparse
from pathlib import Path
from typing import List, Optional

import heifpy


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demux HEIF file.")
    parser.add_argument("path", type=str, help="path2your_file or dir", default=None)
    return parser.parse_args()


def list_from_dir(dir: Path, target_ext: Optional[str] = None) -> List[Path]:
    ret = []
    for fname in dir.glob("*"):
        if target_ext:
            if fname.suffix.lower() == target_ext.lower():
                ret.append(fname)
        else:
            ret.append(fname)
    return ret


def demux(img_path: Path) -> None:
    heif_reader = heifpy.HeifReader(str(img_path))
    item_id_list = heif_reader.get_item_id_list()
    for item_id in item_id_list:
        item_type = heif_reader.get_item_type(item_id)
        if item_type == heifpy.ItemType.GRID:
            continue

        ext = ".xml" if item_type == heifpy.ItemType.XMP else ".bin"
        out_path = f"{img_path.stem}_item_{item_id}_{item_type}{ext}"
        with open(out_path, "wb") as wf:
            item = heif_reader.read_item(item_id)
            wf.write(item)

            print()
            print(f"item_ID     : {item_id}")
            print(f"item_type   : {item_type}")
            print("save :", out_path)

    return


def main(args: argparse.Namespace) -> None:
    in_path = Path(args.path)

    file_paths = []
    if in_path.is_file():
        file_paths = [in_path]
    elif in_path.is_dir():
        file_paths = list_from_dir(Path(in_path), ".heic")

    for img_path in file_paths:
        demux(img_path)


if __name__ == "__main__":
    main(get_args())
