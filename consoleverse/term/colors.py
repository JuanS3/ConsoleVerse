# TEXT COLORS
_CODE_COLOR_BLACK: int   = 30
_CODE_COLOR_RED: int     = 31
_CODE_COLOR_GREEN: int   = 32
_CODE_COLOR_YELLOW: int  = 33
_CODE_COLOR_BLUE: int    = 34
_CODE_COLOR_MAGENTA: int = 35
_CODE_COLOR_CYAN: int    = 36
_CODE_COLOR_WHITE: int   = 37

# BACKGROUND COLORS
_CODE_BACKGROUND_BLACK: int   = 40
_CODE_BACKGROUND_RED: int     = 41
_CODE_BACKGROUND_GREEN: int   = 42
_CODE_BACKGROUND_YELLOW: int  = 43
_CODE_BACKGROUND_BLUE: int    = 44
_CODE_BACKGROUND_MAGENTA: int = 45
_CODE_BACKGROUND_CYAN: int    = 46
_CODE_BACKGROUND_WHITE: int   = 47

_CODE_RESET: int  = 0
_START_COLOR: str = '\033[{}m'
_END_COLOR: str   = _START_COLOR.format(_CODE_RESET)

__COLORS = {
    (BLACK   := 'BLACK')   : _START_COLOR.format(_CODE_COLOR_BLACK),
    (RED     := 'RED')     : _START_COLOR.format(_CODE_COLOR_RED),
    (GREEN   := 'GREEN')   : _START_COLOR.format(_CODE_COLOR_GREEN),
    (YELLOW  := 'YELLOW')  : _START_COLOR.format(_CODE_COLOR_YELLOW),
    (BLUE    := 'BLUE')    : _START_COLOR.format(_CODE_COLOR_BLUE),
    (MAGENTA := 'MAGENTA') : _START_COLOR.format(_CODE_COLOR_MAGENTA),
    (CYAN    := 'CYAN')    : _START_COLOR.format(_CODE_COLOR_CYAN),
    (WHITE   := 'WHITE')   : _START_COLOR.format(_CODE_COLOR_WHITE),
}

COLORS_LIST = list(__COLORS.keys())

__BACKGROUNDS = {
    (BG_BLACK   := 'BG_BLACK')   : _START_COLOR.format(_CODE_BACKGROUND_BLACK),
    (BG_RED     := 'BG_RED')     : _START_COLOR.format(_CODE_BACKGROUND_RED),
    (BG_GREEN   := 'BG_GREEN')   : _START_COLOR.format(_CODE_BACKGROUND_GREEN),
    (BG_YELLOW  := 'BG_YELLOW')  : _START_COLOR.format(_CODE_BACKGROUND_YELLOW),
    (BG_BLUE    := 'BG_BLUE')    : _START_COLOR.format(_CODE_BACKGROUND_BLUE),
    (BG_MAGENTA := 'BG_MAGENTA') : _START_COLOR.format(_CODE_BACKGROUND_MAGENTA),
    (BG_CYAN    := 'BG_CYAN')    : _START_COLOR.format(_CODE_BACKGROUND_CYAN),
    (BG_WHITE   := 'BG_WHITE')   : _START_COLOR.format(_CODE_BACKGROUND_WHITE),
}

BACKGROUNDS_LIST = list(__BACKGROUNDS.keys())

__STYLES = {
    (BOLD      := 'BOLD')      : '\033[1m',
    (UNDERLINE := 'UNDERLINE') : '\033[4m',
    (BLINK     := 'BLINK')     : '\033[5m',
    (INVERT    := 'INVERT')    : '\033[7m',
    (HIDDEN    := 'HIDDEN')    : '\033[8m',
}

STYLES_LIST = list(__STYLES.keys())



def get_color(color: str = '') -> str:
    color = color.upper()
    return __COLORS[color] if color in __COLORS else ''

def get_background(bg_color: str) -> str:
    bg_color = bg_color.upper()
    if 'BG_' not in bg_color:
        bg_color = 'BG_' + bg_color
    return __BACKGROUNDS[bg_color] if bg_color in __BACKGROUNDS else ''

def get_style(style: str) -> str:
    style = style.upper()
    return __STYLES[style] if style in __STYLES else ''

def reset_colors() -> str:
    return _END_COLOR

