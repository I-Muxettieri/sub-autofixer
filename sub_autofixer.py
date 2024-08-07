import re
from typing import Dict, List, Optional
from pysubs2 import SSAEvent, SSAFile, SSAStyle, load as load_sub
import argparse
import os
import subprocess
from utils import parse_style, slipt_stags

TYPESETTING_TAGS_REGEX = r"\\pos|\\move"
OVERRIDE_TAGS_REGEX = r"{\\[^}]+}"


def path_name_normalizer(path: str) -> str:
    norm_path = ""
    for char in path:
        if char == "à":
            norm_path += "a"
        elif char == "è" or char == "é":
            norm_path += "e"
        elif char == "ò":
            norm_path += "o"
        elif char == "ù":
            norm_path += "u"
        else:
            norm_path += char
    return norm_path


def is_valid_sub_file(filename: str) -> bool:
    return filename.endswith(".ass") or filename.endswith(".srt")


def sub_converter(filename: str, output: str) -> str:
    name = os.path.splitext(os.path.basename(filename))
    new_path = path_name_normalizer(
        os.path.normpath(os.path.join(output, f"{name[0]}.ass"))
    )
    subs = load_sub(filename)
    subs.save(new_path, format_="ass")
    return new_path


def resample_script(sub: str, video: str, output: str):
    new_filename = os.path.join(output, os.path.splitext(os.path.basename(sub))[0])
    aegi_resample = [
        "aegisub-cli",
        "--video",
        video,
        sub,
        f"{new_filename}.ass",
        "tool/resampleres",
    ]

    # archi_resample = f'aegisub-cli --loglevel 4 --video "{video}" "{new_filename}" "{new_filename}" "tool/resampleres"'
    res_result = subprocess.run(
        aegi_resample, check=True, capture_output=True, text=True
    )
    # subprocess.run(
    #     archi_resample, shell=True, check=True, capture_output=True, text=True
    # )

    print(res_result.stdout)
    print(res_result.stderr)


def cleanup(sub: str):
    script_cleanup = [
        "aegisub-cli",
        "--selected-lines",
        "0",
        "--dialog",
        '{"button": 0, "values": {"nostyle": true}}',
        "--automation",
        "ua.ScriptCleanup.lua",
        sub,
        sub,
        "Script Cleanup",
    ]

    result = subprocess.run(script_cleanup, check=True, capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)


def is_dialogue_event(event: SSAEvent) -> bool:
    # if (
    #     event.style == "Main"
    #     or event.style == "Main_Italics"
    #     or event.style == "Main_Top"
    #     or event.style == "Main_Top_Italics"
    #     or event.style == "Main_Overlap"
    #     or event.style == "Flashback"
    # ):
    #     return True
    # return False
    tags: List[str] = re.findall(OVERRIDE_TAGS_REGEX, event.text)
    for tag in tags:
        if re.search(TYPESETTING_TAGS_REGEX, tag):
            return False
    return True


def split_dash_overlap(event: SSAEvent) -> list[SSAEvent]:
    start_tags, stripped_text = slipt_stags(event.text)

    overlap_events = []
    if stripped_text.startswith("-"):
        while True:
            break_position = stripped_text.find("\\N")
            if break_position == -1:
                if len(overlap_events):
                    new_event = event.copy()
                    new_event.text = start_tags + stripped_text[1:].strip()
                    overlap_events.append(new_event)
                break
            new_event = event.copy()
            new_event.text = start_tags + stripped_text[1:break_position].strip()
            overlap_events.append(new_event)
            stripped_text = stripped_text[break_position + 2 :].strip()

    return overlap_events


def get_inline_alignment(text: str) -> Optional[int]:
    pattern = r"\\an(\d)"
    match = re.search(pattern, text)
    return int(match.group(1)) if match else None


def restyler(subs: SSAFile, restyling_styles: Dict[str, SSAStyle], dialogue_layer: int):
    subs.styles.update(restyling_styles)

    dialogue_style_name = list(restyling_styles.keys())[0]
    overlap_style_name = (
        list(restyling_styles.keys())[1] if len(restyling_styles) > 1 else None
    )
    dialogue_style = list(restyling_styles.values())[0]
    type_events = []
    dialogue_events: list[SSAEvent] = []

    for i, event in enumerate(subs):
        if not is_dialogue_event(event):
            # add to typesetting events array
            type_events.append(event)
        else:
            # perform restyle
            # change layer
            if dialogue_layer > 0:
                event.layer = dialogue_layer

            # change event style
            event_style = subs.styles[event.style]
            tags = []
            if event_style.alignment != dialogue_style.alignment:
                tags.append(f"\\an{event_style.alignment}")
            if event_style.italic and event_style.italic != dialogue_style.italic:
                tags.append(f"\\i{int(event_style.italic)}")

            if event_style.bold and event_style.bold != dialogue_style.bold:
                tags.append(f"\\b{int(event_style.bold)}")
            if (
                event_style.underline
                and event_style.underline != dialogue_style.underline
            ):
                tags.append(f"\\u{int(event_style.underline)}")
            if (
                event_style.strikeout
                and event_style.strikeout != dialogue_style.strikeout
            ):
                tags.append(f"\\s{int(event_style.strikeout)}")

            event.style = dialogue_style_name
            event.text = ("{" + "".join(tags) + "}" if len(tags) else "") + event.text

            # remove overlap with dash "-"
            overlap_events = split_dash_overlap(event)

            if len(overlap_events) > 2:
                print(f'Warning: {len(overlap_events)} dash "-" overlaps in line {i}')
            elif len(overlap_events) == 1:
                print(f'Warning: only one dash "-" overlap in line {i}')

            # add to dialogue events array
            if len(overlap_events):
                dialogue_events.extend(overlap_events)
            else:
                dialogue_events.append(event)

    # sort dialogue events
    dialogue_events.sort(key=lambda event: event.start)

    # overlap lines
    if overlap_style_name:
        current_overlap: list[Optional[SSAEvent]] = [None for _ in range(9)]
        last_dialog: list[Optional[SSAEvent]] = [None for _ in range(9)]

        for event in dialogue_events:
            inline_an = get_inline_alignment(event.text)
            event_an = inline_an if inline_an else subs.styles[event.style].alignment
            last_dialog_an = last_dialog[event_an]
            current_overlap_an = current_overlap[event_an]

            if not last_dialog_an or event.start >= last_dialog_an.end:
                last_dialog[event_an] = event
            elif not current_overlap_an or event.start >= current_overlap_an.end:
                event.style = overlap_style_name
                current_overlap[event_an] = event
            else:
                event.effect = "Overlap error"
                print(
                    f'Error: there are more than 2 lines in overlap for an{event_an}, set line with "Overlap error" effect'
                )

    subs.events = dialogue_events + type_events


def main():
    parser = argparse.ArgumentParser(description="Fix subs")
    parser.add_argument("input", type=str, help="sub dir or sub file")
    parser.add_argument("-v", "--video", type=str, help="video path, default = None")
    parser.add_argument(
        "-o", "--output", type=str, help="output path, defaiult = 'output'"
    )
    parser.add_argument(
        "-l",
        "--layer",
        type=int,
        help="dialogue layer, set to -1 to not change layers, default = 90",
    )

    args = parser.parse_args()
    input: str = os.path.normpath(args.input)
    filenames: List[str] = []
    video: Optional[str] = args.video
    output: str = "output"
    layer: int = 90

    if os.path.isdir(input):
        for filename in os.listdir(input):
            if is_valid_sub_file(filename):
                filenames.append(os.path.join(input, filename))

    elif os.path.isfile(input) and is_valid_sub_file(input):
        filenames.append(input)
    else:
        raise Exception("Sub file err")

    if video and not os.path.isfile(video):
        video = None
    if args.output:
        output = args.output
    if args.layer:
        layer = args.layer

    os.makedirs(output, exist_ok=True)

    restyling_styles = {}
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "styles.txt"), "r"
    ) as styles:
        for style in styles:
            restyling_styles.update(parse_style(style.strip()))

    for filename in filenames:
        print(f"Fixing: {filename}")

        filename = sub_converter(filename, output)

        if video:
            resample_script(filename, video, output)

        subs = load_sub(filename)

        if len(restyling_styles):
            restyler(subs, restyling_styles, layer)

        subs.save(os.path.join(output, os.path.basename(filename)), format_="ass")

        cleanup(filename)


if __name__ == "__main__":
    main()
