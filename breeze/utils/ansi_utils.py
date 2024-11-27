import re


FG_COLOR_TEMPLATE = "\x1b[38;5;{}m"
BG_COLOR_TEMPLATE = "\x1b[48;5;{}m"

NAMED_COLORS = {
    "black": 0,
    "red": 1,
    "green": 2,
    "yellow": 3,
    "blue": 4,
    "magenta": 5,
    "cyan": 6,
    "white": 7,
    "bright_red": 9,
    "bright_green": 10,
    "bright_yellow": 11,
    "bright_blue": 12,
    "bright_magenta": 13,
    "bright_cyan": 14,
    "bright_white": 15,
}

STYLES = {
    "BOLD": "\x1b[1m",
    "UNDERLINE": "\x1b[4m",
    "RESET": "\x1b[0m",
}


def colorise(text, color=None, background=None, bold=False, underline=False):
    style_codes = []

    if color is not None:
        if isinstance(color, int):
            style_codes.append(FG_COLOR_TEMPLATE.format(color))
        elif color.lower() in NAMED_COLORS:
            style_codes.append(FG_COLOR_TEMPLATE.format(NAMED_COLORS[color.lower()]))
        elif color.is_digit():
            style_codes.append(FG_COLOR_TEMPLATE.format(int(color)))

    if background is not None:
        if isinstance(background, int):
            style_codes.append(BG_COLOR_TEMPLATE.format(background))
        elif background.lower() in NAMED_COLORS:
            style_codes.append(
                BG_COLOR_TEMPLATE.format(NAMED_COLORS[background.lower()])
            )
        elif background.isdigit():
            style_codes.append(BG_COLOR_TEMPLATE.format(int(background)))

    if bold:
        style_codes.append(STYLES["BOLD"])

    if underline:
        style_codes.append(STYLES["UNDERLINE"])

    style_start = "".join(style_codes)
    style_end = STYLES["RESET"]

    return f"{style_start}{text}{style_end}"


def strip_ansi_codes(text):
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def print_color_palette():
    for i in range(0, 256):
        print(f"\x1b[38;5;{i}m {i:>3} \x1b[0m", end=" ")
        if (i + 1) % 16 == 0:
            print()
    print("\n\nGrayscale colors:")
    for i in range(232, 256):
        print(f"\x1b[48;5;{i}m {i:>3} \x1b[0m", end=" ")
    print("\x1b[0m")


if __name__ == "__main__":
    mood_chart_colors = [40, 120, 226, 208, 160, 1]
    mood_chart_scale = []
    for color in mood_chart_colors:
        mood_chart_scale.append(colorise("\U0001F60A", color=color))
    print(" ".join(mood_chart_scale))
    print("\033[92m\u25CF\033[0m - Very Happy")
