from typing import Dict
from pysubs2 import Color, Alignment, SSAStyle


def parse_color(color: str) -> Color:
    parsed_color = color
    if parsed_color.startswith("&H"):
        parsed_color = color[2:]
    elif parsed_color.startswith("H"):
        parsed_color = color[1:]
    if parsed_color.endswith("H"):
        parsed_color = parsed_color[:1]

    red = 0
    green = 0
    blue = 0
    alpha = 0
    if len(parsed_color) > 6:
        alpha = int(parsed_color[:2], 16)
        red = int(parsed_color[6:8], 16)
        green = int(parsed_color[4:6], 16)
        blue = int(parsed_color[2:4], 16)
    else:
        red = int(parsed_color[4:6], 16)
        green = int(parsed_color[2:4], 16)
        blue = int(parsed_color[:2], 16)

    return Color(red, green, blue, alpha)


def parse_style(style: str) -> Dict[str, SSAStyle]:
    if not style.startswith("Style: "):
        return {}
    style = style[7:]
    parts = style.split(",")

    parsed_style = SSAStyle()

    parsed_style.fontname = parts[1]
    parsed_style.fontsize = float(parts[2])
    parsed_style.primarycolor = parse_color(parts[3])
    parsed_style.secondarycolor = parse_color(parts[4])
    parsed_style.outlinecolor = parse_color(parts[5])
    parsed_style.backcolor = parse_color(parts[6])
    parsed_style.bold = parts[7] != "0"
    parsed_style.italic = parts[8] != "0"
    parsed_style.underline = parts[9] != "0"
    parsed_style.strikeout = parts[10] != "0"
    parsed_style.scalex = float(parts[11])
    parsed_style.scaley = float(parts[12])
    parsed_style.spacing = float(parts[13])
    parsed_style.angle = float(parts[14])
    parsed_style.borderstyle = int(parts[15])
    parsed_style.outline = float(parts[16])
    parsed_style.shadow = float(parts[17])
    parsed_style.alignment = Alignment(int(parts[18]))
    parsed_style.marginl = int(parts[19])
    parsed_style.marginr = int(parts[20])
    parsed_style.marginv = int(parts[21])
    parsed_style.encoding = int(parts[22])

    return {parts[0]: parsed_style}


def slipt_stags(text: str) -> tuple[str, str]:
    start_tags = ""
    tag_section = False
    for i, char in enumerate(text):
        if char == "{":
            tag_section = True
            start_tags += char
        elif char == "}":
            tag_section = False
            start_tags += char
        elif tag_section:
            start_tags += char
        elif not tag_section:
            return (start_tags, text[i:].strip())
    return ("", "")
