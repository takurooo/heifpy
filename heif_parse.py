import argparse

import heifpy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse HEIF file.")
    parser.add_argument("img_path", type=str, help="path2your_image", default=None)
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    heif_reader = heifpy.HeifReader(args.img_path)
    heif_reader.print_boxes()


if __name__ == "__main__":
    main(parse_args())
