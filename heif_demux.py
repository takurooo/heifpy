# -----------------------------------
# import
# -----------------------------------
import os
import argparse
import heifpy
from .listutils import list_from_dir

# -----------------------------------
# define
# -----------------------------------


# -----------------------------------
# function
# -----------------------------------
def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demux HEIF file.")
    parser.add_argument("path", type=str, help="path2your_file or dir", default=None)
    return parser.parse_args()


def demux(img_path: str) -> None:
    heif_reader = heifpy.HeifReader(img_path)
    item_id_list = heif_reader.get_item_id_list()

    basename, _ = os.path.splitext(img_path)

    for item_id in item_id_list:
        item_type = heif_reader.get_item_type(item_id)
        if item_type == heifpy.ItemType.GRID:
            continue

        ext = ".xml" if item_type == heifpy.ItemType.XMP else ".bin"

        out_path = f"{basename}_item_{item_id}_{item_type}{ext}"
        with open(out_path, "wb") as wf:
            item = heif_reader.read_item(item_id)
            wf.write(item)

            print()
            print(f"item_ID     : {item_id}")
            print(f"item_type   : {item_type}")
            print("save :", out_path)

    return


# -----------------------------------
# main
# -----------------------------------
def main(args: argparse.Namespace) -> None:
    in_path = args.path

    file_paths = []
    if os.path.isfile(in_path):
        file_paths = [in_path]
    elif os.path.isdir(in_path):
        # フォルダが指定された場合はフォルダ内のfileを全て変換対象とする.
        file_paths = list_from_dir(in_path)

    for img_path in file_paths:
        demux(img_path)


if __name__ == "__main__":
    main(get_args())
