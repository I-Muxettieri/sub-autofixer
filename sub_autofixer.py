from typing import List, Optional
import pysubs2
import argparse
import os
import subprocess


def resample_script(sub: str, video: str, output: str):
    new_filename = os.path.join(output, os.path.splitext(os.path.basename(sub))[0])
    command = f'aegisub-cli --loglevel 4 --video "{video}" "{sub}" "{new_filename}.ass" "tool/resampleres"'
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)


def is_valid_sub_file(filename: str) -> bool:
    return filename.endswith(".ass") or filename.endswith(".srt")


def sub_converter(filename: str, output: str):
    name = os.path.splitext(os.path.basename(filename))
    new_path = os.path.join(output, f"{name[0]}.ass")
    subs = pysubs2.load(filename)
    subs.save(new_path, format_="ass")
    return new_path


def main():
    parser = argparse.ArgumentParser(description="Fix subs")
    parser.add_argument("input", type=str, help="sub dir or sub file")
    parser.add_argument("-v", "--video", type=str, help="video path")
    parser.add_argument("-o", "--output", type=str, help="output path")

    args = parser.parse_args()
    input: str = os.path.normpath(args.input)
    filenames: List[str] = []
    video: Optional[str] = args.video
    output: str = "output"

    if video and not os.path.isfile(video):
        video = None
    if args.output:
        output = args.output

    os.makedirs(output, exist_ok=True)

    if os.path.isdir(input):
        for filename in os.listdir(input):
            if is_valid_sub_file(filename):
                filenames.append(os.path.join(input, filename))

    elif os.path.isfile(input) and is_valid_sub_file(input):
        filenames.append(input)
    else:
        raise Exception("Sub file err")

    for filename in filenames:
        print(f"Fixing: {filename}")

        if not filename.endswith(".ass"):
            filename = sub_converter(filename, output)

        if video:
            resample_script(filename, video, output)


if __name__ == "__main__":
    main()
