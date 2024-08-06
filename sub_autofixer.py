import re
from typing import Dict, List, Optional
from pysubs2 import SSAEvent, SSAStyle, load as load_sub
import argparse
import os
import subprocess
from utils import parse_style

TYPESETTING_TAGS_REGEX = r"\\pos|\\move"
OVERRIDE_TAGS_REGEX = r"{\\[^}]+}"


def is_valid_sub_file(filename: str) -> bool:
    return filename.endswith(".ass") or filename.endswith(".srt")


def sub_converter(filename: str, output: str) -> str:
    name = os.path.splitext(os.path.basename(filename))
    new_path = os.path.join(output, f"{name[0]}.ass")
    subs = load_sub(filename)
    subs.save(new_path, format_="ass")
    return new_path


def resample_script(sub: str, video: str, output: str):
    new_filename = os.path.join(output, os.path.splitext(os.path.basename(sub))[0])
    aegi_resample = f'aegisub-cli --loglevel 4 --video "{video}" "{sub}" "{new_filename}.ass" "tool/resampleres"'
    # archi_resample = f'aegisub-cli --loglevel 4 --video "{video}" "{new_filename}" "{new_filename}" "tool/resampleres"'
    subprocess.run(
        aegi_resample, shell=True, check=True, capture_output=True, text=True
    )
    # subprocess.run(
    #     archi_resample, shell=True, check=True, capture_output=True, text=True
    # )


def is_dialogue_line(line: SSAEvent) -> bool:
    tags: List[str] = re.findall(OVERRIDE_TAGS_REGEX, line.text)
    for tag in tags:
        if re.search(TYPESETTING_TAGS_REGEX, tag):
            return False
    return True


def restyle_dialogue(filename: str, output: str, restyling_styles: Dict[str, SSAStyle]):
    subs = load_sub(filename)

    subs.styles.update(restyling_styles)

    for line in subs:
        if is_dialogue_line(line):
            line.style = list(restyling_styles.keys())[0]

    subs.save(os.path.join(output, os.path.basename(filename)), format_="ass")


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

    restyling_styles = {}
    with open("styles.txt", "r") as styles:
        for style in styles:
            restyling_styles.update(parse_style(style.strip()))

    for filename in filenames:
        print(f"Fixing: {filename}")

        filename = sub_converter(filename, output)

        if video:
            resample_script(filename, video, output)

        if len(restyling_styles):
            restyle_dialogue(filename, output, restyling_styles)


if __name__ == "__main__":
    main()
