#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path


def reverse_text(input_file: Path) -> str:
    """Reverses the lines of a text file.

    Args:
        input_file: The path to the input file.
        output_file: The path to the output file.
    """

    text = input_file.read_text()
    for switch in ("(", ")"), ("[", "]"), ("{", "}"), ("<", ">"), ("/", "\\"):
        fst, snd = switch
        text = text.replace(fst, "TEMP").replace(snd, fst).replace("TEMP", snd)

    lines = text.splitlines()
    lines = [line[::-1] for line in lines]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Process some files.")

    parser.add_argument(
        "input_files",
        metavar="input files",
        type=str,
        nargs="+",
        help="input files to be processed",
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        type=str,
        metavar="OUTPUT_FILE",
        help="output file where the result will be saved",
    )

    args = parser.parse_args()

    output = open(args.output_file, "w") if args.output_file else sys.stdout

    try:
        for input_file in args.input_files:
            output.write(reverse_text(Path(input_file).resolve()))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        output.close()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
