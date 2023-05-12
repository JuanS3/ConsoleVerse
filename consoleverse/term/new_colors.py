from term.exceptions.ex_colors import (
    ColorTextError,
    ColorBackgroundError,
    ColorStyleError
)


class _ColorBase:
    RESET_FORMAT_COLOR: int = 0
    START_FORMAT_COLOR: str = '\033[{}m'
    END_FORMAT_COLOR: str   = START_FORMAT_COLOR.format(RESET_FORMAT_COLOR)

    def start(self, color):
        return self.START_FORMAT_COLOR.format(color)

    def end(self):
        return self.END_FORMAT_COLOR

    def reset(self):
        return self.END_FORMAT_COLOR


class ColorTextCode(_ColorBase):
    BLACK_CODE: int   = 30
    RED_CODE: int     = 31
    GREEN_CODE: int   = 32
    YELLOW_CODE: int  = 33
    BLUE_CODE: int    = 34
    MAGENTA_CODE: int = 35
    CYAN_CODE: int    = 36
    WHITE_CODE: int   = 37


class ColorText(ColorTextCode):

    def __init__(self):
        self.COLORS = {
            (self.BLACK   := 'BLACK')   : self.start(self.BLACK_CODE),
            (self.RED     := 'RED')     : self.start(self.RED_CODE),
            (self.GREEN   := 'GREEN')   : self.start(self.GREEN_CODE),
            (self.YELLOW  := 'YELLOW')  : self.start(self.YELLOW_CODE),
            (self.BLUE    := 'BLUE')    : self.start(self.BLUE_CODE),
            (self.MAGENTA := 'MAGENTA') : self.start(self.MAGENTA_CODE),
            (self.CYAN    := 'CYAN')    : self.start(self.CYAN_CODE),
            (self.WHITE   := 'WHITE')   : self.start(self.WHITE_CODE),
        }

        self.COLORS_LIST = list(self.COLORS.keys())

    def __getitem__(self, color):
        try:
            return self.COLORS[color.upper()]
        except KeyError:
            raise ColorTextError(color)

    def __contains__(self, color):
        return color.upper() in self.COLORS

    def __str__(self):
        return str(self.COLORS_LIST)


class ColorBackgroundCode(_ColorBase):
    BG_BLACK_CODE: int   = 40
    BG_RED_CODE: int     = 41
    BG_GREEN_CODE: int   = 42
    BG_YELLOW_CODE: int  = 43
    BG_BLUE_CODE: int    = 44
    BG_MAGENTA_CODE: int = 45
    BG_CYAN_CODE: int    = 46
    BG_WHITE_CODE: int   = 47


class ColorBackground(ColorBackgroundCode):

    def __init__(self):
        self.BACKGROUNDS = {
            (self.BG_BLACK   := 'BG_BLACK')   : self.start(self.BG_BLACK_CODE),
            (self.BG_RED     := 'BG_RED')     : self.start(self.BG_RED_CODE),
            (self.BG_GREEN   := 'BG_GREEN')   : self.start(self.BG_GREEN_CODE),
            (self.BG_YELLOW  := 'BG_YELLOW')  : self.start(self.BG_YELLOW_CODE),
            (self.BG_BLUE    := 'BG_BLUE')    : self.start(self.BG_BLUE_CODE),
            (self.BG_MAGENTA := 'BG_MAGENTA') : self.start(self.BG_MAGENTA_CODE),
            (self.BG_CYAN    := 'BG_CYAN')    : self.start(self.BG_CYAN_CODE),
            (self.BG_WHITE   := 'BG_WHITE')   : self.start(self.BG_WHITE_CODE),
        }

        self.BACKGROUNDS_LIST = list(self.BACKGROUNDS.keys())

    def __getitem__(self, background):
        try:
            return self.BACKGROUNDS[background.upper()]
        except KeyError:
            raise ColorBackgroundError(background)

    def __contains__(self, background):
        return background.upper() in self.BACKGROUNDS

    def __str__(self):
        return str(self.BACKGROUNDS_LIST)


class ColorStyleCode(_ColorBase):
    BOLD_CODE: int       = 1
    UNDERLINE_CODE: int  = 4
    BLINK_CODE: int      = 5
    REVERSE_CODE: int    = 7
    CONCEAL_CODE: int    = 8


class ColorStyle(ColorStyleCode):

    def __init__(self):
        self.STYLES = {
            (self.BOLD      := 'BOLD')      : self.start(self.BOLD_CODE),
            (self.UNDERLINE := 'UNDERLINE') : self.start(self.UNDERLINE_CODE),
            (self.BLINK     := 'BLINK')     : self.start(self.BLINK_CODE),
            (self.REVERSE   := 'REVERSE')   : self.start(self.REVERSE_CODE),
            (self.CONCEAL   := 'CONCEAL')   : self.start(self.CONCEAL_CODE),
        }

        self.STYLES_LIST = list(self.STYLES.keys())

    def __getitem__(self, style):
        try:
            return self.STYLES[style.upper()]
        except KeyError:
            raise ColorStyleError(style)

    def __contains__(self, style):
        return style.upper() in self.STYLES

    def __str__(self):
        return str(self.STYLES_LIST)