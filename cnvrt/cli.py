from __future__ import annotations
import os
import subprocess
import argparse
import json
import sys
from pprint import pprint

import filetype as ft
import send2trash as stt


this = __file__
here = os.path.dirname(__file__)
settings_file_path = os.path.join(here, "settings.json")

DEFAULT_FORMAT = "ogg"
DEFAULT_BITRATE = 450


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("error: %s\n" % message)
        self.print_help(sys.stderr)
        sys.exit(1 if len(sys.argv) == 1 else 2)


def load_settings(path: str) -> dict[str | str]:
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return dict()


def save_settings(path: str, data: dict) -> type(None):
    with open(path, "w") as f:
        json.dump(data, f, indent=2 * " ", sort_keys=True)


settings = load_settings(settings_file_path)
sample_folder = settings.get("sample_folder")


def convert(file, new_format=".mp3", quality=320) -> str:
    new_format = "." + new_format if new_format[0] != "." else new_format

    name = os.path.splitext(os.path.split(file)[1])[0]
    folder = os.sep.join(file.split(os.sep)[:-1])
    new = os.path.join(folder, name + new_format)

    cmd = [
        "ffmpeg",
        "-y",
        "-hide_banner",
        "-v",
        "info",
        "-i",
        file,
        "-ab",
        str(quality * 1000),
        new,
    ]
    subprocess.run(cmd)
    print("\n" * 5)
    return new


def metadata(file: str) -> dict[str, str | int | float | dict[str, str | int]]:
    data = subprocess.getoutput(
        f'ffprobe -hide_banner -v quiet -print_format json -bitexact -show_format -show_streams -pretty -i "{file}"'
    )
    return json.loads(data)


def get_sample_dir() -> str:
    pth = settings.get("sample_folder")
    while None == pth:
        pth = input(
            "\nWhere do you want to keep your samples? (tree will be generated"
            " automatically):\n\t"
        )
    pth = validPath(pth)
    os.makedirs(pth, exist_ok=True)
    return pth


def handle(args: argparse.Namespace, original: str, product: str) -> type(None):
    if args.sample:
        settings["sample_folder"] = sample_folder = get_sample_dir()
        save_settings(settings_file_path, settings)

        _, name = os.path.split(product)
        os.rename(product, os.path.join(sample_folder, name))

    if args.discard or args.recycle:
        stt.send2trash(original) if args.recycle else os.remove(original)


def audio(path: str, matters: bool) -> bool:
    if matters:
        return ft.audio_match(path) or path.endswith(".m4a")
    return True


def audio(path: str, matters: bool) -> bool:
    if matters:
        return ft.audio_match(path) or path.endswith(".m4a")
    return True


def metahandle(args: argparse.Namespace, path: str) -> type(None):
    if args.video:
        if not video(path=path, matters=args.video):
            return
    elif args.audio:
        if not audio(path=path, matters=args.audio):
            return
    out = convert(path, new_format=args.format, quality=args.quality)
    handle(args=args, original=path, product=out)


def validPath(argument: str) -> str:
    if os.path.exists(argument):
        return os.path.abspath(argument)
    elif argument == "":
        return argument
    raise FileNotFoundError(f'Couldn\'t find "{argument}" in the file system')


def main():
    global validPath
    parser = MyParser(description="Convert files with ffmpeg")
    parser.add_argument(
        "paths",
        default="",
        type=validPath,
        nargs="*",
        help="path(s) to the file(s) you wish to convert",
    )
    parser.add_argument(
        "-f",
        "--format",
        default=DEFAULT_FORMAT,
        type=str,
        help=f"new format for the file(s) [default={DEFAULT_FORMAT}]",
    )
    parser.add_argument(
        "-q",
        "--quality",
        default=DEFAULT_BITRATE,
        type=int,
        help=f"quality (in kbps) of the output file(s) [default={DEFAULT_BITRATE}]",
    )
    parser.add_argument(
        "-d",
        "--discard",
        default=False,
        action="store_true",
        help="Remove the original from the filesystem after conversion",
    )
    parser.add_argument(
        "-s",
        "--sample",
        default=False,
        action="store_true",
        help="Add file to sample library",
    )
    parser.add_argument(
        "-c",
        "--config",
        default=False,
        action="store_true",
        help="Print path to settings file",
    )
    parser.add_argument(
        "-a",
        "--audio",
        default=False,
        action="store_true",
        help="Ignore any paths that don't refer to audio files",
    )
    parser.add_argument(
        "-v",
        "--video",
        default=False,
        action="store_true",
        help="Ignore any paths that don't refer to video files",
    )
    parser.add_argument(
        "-r",
        "--recycle",
        default=False,
        action="store_true",
        help="Send the original to the recycle bin after conversion",
    )

    args = parser.parse_args()

    # for validPath in args.paths:
    #     pprint(metadata(validPath))
    # return
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        if args.config:
            print(settings_file_path)
        for p in [i for i in args.paths if i.strip() != "/home"]:
            if os.path.isdir(p):
                for name in os.listdir(p):
                    src = os.path.join(p, name)
                    metahandle(args, src)
            elif os.path.isfile(p):
                metahandle(args, p)


if __name__ == "__main__":
    main()
