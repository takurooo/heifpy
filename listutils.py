import codecs
import os
import re
from typing import Any, Iterator, List, Optional


CUR_PATH = os.path.join(os.path.dirname(__file__))


def list_to_file(fpath, list: Iterator[Any]) -> None:
    with codecs.open(fpath, "w", "utf-8") as f:
        for line in list:
            f.write(line + "\n")


def list_from_file(fpath: str) -> List[str]:
    with codecs.open(fpath, "r", "utf-8") as f:
        lines = f.read().split()
    return lines


def key_sort_by_num(x: str) -> List[int]:
    re_list = re.findall(r"[0-9]+", x)
    re_list = list(map(int, re_list))
    return re_list


def list_from_dir(dir, target_ext: Optional[str] = None) -> List[str]:
    ret_list = []
    fnames = os.listdir(dir)
    fnames = sorted(fnames, key=key_sort_by_num)
    for fname in fnames:
        if target_ext is None:
            path = os.path.join(dir, fname)
            ret_list.append(path)
        else:
            _, ext = os.path.splitext(fname)
            if ext.lower() in target_ext:
                path = os.path.join(dir, fname)
                ret_list.append(path)
    return ret_list


if __name__ == "__main__":
    pass
