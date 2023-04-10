import argparse
from pathlib import Path
from typing import List, Union

import heifpy


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for the demux_heif script.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Demux HEIF file.")
    parser.add_argument(
        "file_or_dir_path",
        type=str,
        help="Path to your HEIF file or directory containing HEIF files.",
    )
    return parser.parse_args()


def get_files_with_target_ext_from_dir(
    directory: Path, target_ext: Union[List[str], None] = None
) -> List[Path]:
    """Get a list of files with specified extensions from a directory.

    Args:
        dir (Path): The directory to search for files.
        target_ext (Union[List[str], None]): A list of target file extensions. If None, all files will be returned.

    Returns:
        List[Path]: A list of files with specified extensions.
    """
    files = directory.glob("*")
    if target_ext:
        files_list = [fname for fname in files if fname.suffix in target_ext]
    else:
        files_list = list(files)
    return files_list


def get_ext_by_item_type(item_type: heifpy.ItemType) -> str:
    """Get file extension by item type.

    Args:
        item_type (heifpy.ItemType): The item type.

    Returns:
        str: The file extension.
    """
    ext = ".xml" if item_type == heifpy.ItemType.XMP else ".bin"
    return ext


def build_output_path(img_path: Path, item_id: int, item_type: heifpy.ItemType) -> Path:
    """Create an output path for the demuxed item based on the input image path, item ID, and item type.

    Args:
        img_path (Path): The path to the input HEIF image file.
        item_id (int): The ID of the item to be extracted from the HEIF image file.
        item_type (heifpy.ItemType): The type of the item to be extracted from the HEIF image file.

    Returns:
        Path: The output path for the demuxed item with the appropriate file extension.
    """
    ext = get_ext_by_item_type(item_type)
    return img_path.parent.joinpath(f"{img_path.stem}_item_{item_id}_{item_type}{ext}")


def write_item(item: bytes, out_path: Path) -> None:
    """Write a byte stream to a file.

    Args:
        item (bytes): The byte stream to be written to the file.
        out_path (Path): The output path for the file.

    Returns:
        None
    """
    with open(out_path, "wb") as wf:
        wf.write(item)


def demux(img_path: Path) -> None:
    """Demux a HEIF image file and save its items as separate files.

    Args:
        img_path (Path): The path to the HEIF image file to be demuxed.

    Returns:
        None

    Side Effects:
        - For each item in the HEIF file, creates a new file with the item's data
          and a filename pattern: "{img_path.stem}_item_{item_id}_{item_type}{ext}".
        - Prints information about each item, including item ID, item type, and output path.
    """
    try:
        heif_reader = heifpy.HeifReader(str(img_path))
    except Exception as e:
        print(f"Error initializing HeifReader: {e}")
        return
    item_id_list = heif_reader.get_item_id_list()
    for item_id in item_id_list:
        item_type = heif_reader.get_item_type(item_id)
        if item_type == heifpy.ItemType.GRID:
            continue

        out_path = build_output_path(img_path, item_id, item_type)
        try:
            item = heif_reader.read_item(item_id)
        except Exception as e:
            print(f"Error reading item {item_id}: {e}")
            continue

        write_item(item, out_path)
        print(f"Item ID: {item_id}\nItem Type: {item_type}\nSave: {out_path}\n")

    return


def main(args: argparse.Namespace) -> None:
    in_path = Path(args.file_or_dir_path)

    file_paths = []
    if in_path.is_file():
        file_paths = [in_path]
    elif in_path.is_dir():
        file_paths = get_files_with_target_ext_from_dir(Path(in_path), [".heic"])

    for img_path in file_paths:
        demux(img_path)


if __name__ == "__main__":
    main(parse_args())
