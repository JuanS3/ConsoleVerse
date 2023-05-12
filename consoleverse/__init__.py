from typing import Any, List, Union
import functools
import platform
import os

from consoleverse import config as cfg
from consoleverse.term import *


"""
Private variables
"""
class ConsoleConfig:
    indentation_type  : str  = ' '
    indentation_lvl   : str  = ''
    indentantion_size : int  = 2
    is_start_console  : bool = False
    autoreset_colors  : bool = True

__START_LANGS = {
    cfg.ENG : 'START',
    cfg.ESP : 'INICIA',
}

__END_LANGS = {
    cfg.ENG : 'END',
    cfg.ESP : 'TERMINA',
}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                         decorators                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def block(message_block: Union[str, dict],
          color: str = BLUE,
          bg_color: str = ''
          ) -> callable:
    """
    Decorator to create a block of text.

    Parameters
    ----------
    message_block : Union[str, dict]
        if is a str, then is the title of the block, if is a dict, then is the
        title is taken according to the language selected in the config file,
        e.g. {'en': 'Title', 'es': 'Título'} the title is printed is Title if the
        language is `en`, and Título if the language is `es`.

    color : str, optional
        The color of the message, by default BLUE

    bg_color : str, optional
        The background color of the message, by default has no color
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            message = message_block
            if isinstance(message_block, dict):
                message = message_block[cfg.lang()]

            start_block(message, color=color, bg_color=bg_color)
            new_line()
            value = func(*args, **kwargs)
            new_line()
            end_block(message, color=color, bg_color=bg_color)
            return value
        return wrapped
    return decorator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          functions                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def __start_console():
    """
    If the console still doesn't start, then start the console without
    clearing the screen, but do nothing if the console is started
    """
    if not ConsoleConfig.is_start_console:
        start_console(False)


def start_console(
        clear: bool = True,
        indentation_type: str = ' ',
        indentation_size: int = 2,
        autoreset_colors: bool = True
        ) -> None:
    """
    Initialize the console, and resert the indentation level

    Parameters
    ----------
    clear : bool, optional
        True to clear the screen and False is not, by default True
    """
    ConsoleConfig.indentation_lvl = ''
    ConsoleConfig.indentantion_size = indentation_size
    ConsoleConfig.indentation_type  = indentation_type
    ConsoleConfig.autoreset_colors  = autoreset_colors

    if clear:
        clear_screen()
    ConsoleConfig.is_start_console = True


def clear_screen():
    """
    Clear the console screen
    """
    os.system('clear' if platform.system() != 'Windows' else 'cls')


def add_lvl():
    """
    Add one level (indentation)
    """
    ConsoleConfig.indentation_lvl += (ConsoleConfig.indentation_type * ConsoleConfig.indentantion_size)


def del_lvl():
    """
    Substract one level (indentation)
    """
    ConsoleConfig.indentation_lvl = ConsoleConfig.indentation_lvl[:-ConsoleConfig.indentantion_size]


def _colorize(text: str,
              color: str,
              bg_color: str,
              style: str,
              reset_console_colors: bool,
              ) -> str:
    """
    Colorize the text

    Parameters
    ----------
    text : str
        The text to colorize

    color : str
        The color of the text, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    bg_color : str
        The background color of the text, the color must be one of the `BACKGROUNS_LIST`
        or `COLORS_LIST` for all colors available; by default has no color

    style : str
        The style of the text, the style must be one of the `STYLES_LIST`,
        by default has no style

    reset_console_colors : bool
        True to reset all colors, False is not necessary, by default `True`

    Returns
    -------
    str
        The colorized text
    """
    colorized_text = get_color(color) + \
                     get_background(bg_color) + \
                     get_style(style) + \
                     text
    if reset_console_colors:
        colorized_text += reset_colors()

    return colorized_text


def println(*message: Any,
            endl: str = '\n',
            withlvl: bool = True,
            color: str = '',
            bg_color: str = '',
            reset_all_colors: bool = True,
            style: str = '',
            sep: str = ' '
            ) -> None:
    """
    Print the message to the console, the `endl` is the same as `end` in print function
    and is necessary print the message with the current indentation level and the color
    indicate.

    Parameters
    ----------
    message : Any
        Message to print to console

    endl : str, optional
        The end of line, by default `\\n`

    withlvl : bool, optional
        True if the message should be printed with the current indentation
        False is not necessary, by default `True`

    color : str, optional
        The color of the message, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    bg_color : str, optional
        The background color of the message, the color must be one of the `BACKGROUNS_LIST`
        or `COLORS_LIST` for all colors available; by default has no color

    reset_all_colors : bool, optional
        True to reset all colors, False is not necessary, by default `True`

    style : str, optional
        The style of the message, the style must be one of the `STYLES_LIST`,
        by default has no style

    sep : str, optional
        The separator between the values, by default is a space
    """
    __start_console()
    message = __to_string(*message, sep=sep)

    if withlvl:
        message = ConsoleConfig.indentation_lvl + message

    reset_console_colors: str = reset_colors() if reset_all_colors or ConsoleConfig.autoreset_colors else ''
    colorized_text: str = _colorize(text=message,
                                    color=color,
                                    bg_color=bg_color,
                                    style=style,
                                    reset_console_colors=reset_console_colors
                                    )
    print(colorized_text, end=endl)


def __to_string(*values: Any, sep: str = ' ') -> str:
    return sep.join([str(m) for m in values])


def start_block(*message: Any, color: str = BLUE, bg_color: str = '') -> None:
    """
    Start a block of messages

    Parameters
    ----------
    message : Any
        The title of the block

    color : str, optional
        The color of the title block, by default BLUE

    bg_color : str, optional
        The background color of the title block, by default has no color
    """
    message = __to_string(*message)
    println(f'{__START_LANGS[cfg.lang()]} {message.upper()}',
            color=color,
            bg_color=bg_color
            )
    add_lvl()


def end_block(*message: Any,
              color: str = BLUE,
              bg_color: str = '',
              style: str = ''
              ) -> None:
    """
    End a block of messages

    Parameters
    ----------
    message : Any
        The title of the block

    color : str, optional
        The color of the title block, by default BLUE

    bg_color : str, optional
        The background color of the title block, by default has no color

    style : str, optional
        The style of the title block, by default has no style
    """
    message = __to_string(*message)
    del_lvl()
    println(f'{__END_LANGS[cfg.lang()]} {message.upper()}',
            color=color,
            bg_color=bg_color,
            style=style
            )
    new_line()


def warning(*message: Any,
            color: str = BLUE,
            bg_color: str = '',
            style: str = ''
            ) -> None:
    """
    Warning message starts with 'warning: {message}'

    Parameters
    ----------
    message : Any
        The message to display in the log

    color : str, optional
        The color of the message, by default YELLOW

    bg_color : str, optional
        The background color of the message, by default has no color

    style : str, optional
        The style of the message, by default has no style
    """
    message = __to_string(*message)
    println(f'warning: {message}', color=color, bg_color=bg_color, style=style)


def error(*message: Any,
          color: str = RED,
          bg_color: str = '',
          style: str = ''
          ) -> None:
    """
    Error message is displayed like `error: >>> {message} <<<`

    Parameters
    ----------
    message : Any
        The message to display in the log

    color : str, optional
        The color of the message, by default RED

    bg_color : str, optional
        The background color of the message, by default has no color

    style : str, optional
        The style of the message, by default has no style
    """
    message = __to_string(*message)
    println(f'error: >>> {message} <<<', color=color, bg_color=bg_color, style=style)


def new_line():
    """
    Display a blank line in the console
    """
    println('', withlvl=False)


def line(size: int = 30,
         style: str = '-- ',
         color: str = '',
         bg_color: str = '',
         style_text: str = ''
         ) -> None:
    """
    Display a line in the console like this `-- -- -- -- -- -- --`
    whit the indicated size

    Parameters
    ----------
    size : int, optional
        The size of the line to display, by display 30

    style : str, optional
        The style of the line, by default is '-- '

    color : str, optional
        The color of the line, by default has no color

    bg_color : str, optional
        The background color of the line, by default has no color

    style_text : str, optional
        The style of the line, by default has no style
    """
    line: str = style * size
    if line[:-1] == ' ':
        line = line[:-1]
    println(line, color=color, bg_color=bg_color, style=style_text)
    new_line()


def print_emoji_list() -> None:
    """
    Print the list of emojis available
    """
    println('Emojis available:')
    add_lvl()
    for e in EMOJIS_LIST:
        println(f'{emoji(e):2} : {e}')
    del_lvl()


def print_color_list() -> None:
    """
    Print the list of colors available in the console
    """
    println('Colors available:')
    add_lvl()
    for e in COLORS_LIST:
        println(f'{e:7} : ', endl='')
        println('ConsoleVerse', color=e, withlvl=False)
    del_lvl()
    new_line()

    print('Background colors available:')
    add_lvl()
    for e in BACKGROUNDS_LIST:
        println(f'{e:10} : ', endl='')
        println('ConsoleVerse', bg_color=e, withlvl=False)
    del_lvl()

def print_style_list() -> None:
    """
    Print the list of styles available in the console
    """
    println('Styles available:')
    add_lvl()
    for e in STYLES_LIST:
        println(f'{e:10} : ', endl='')
        println('ConsoleVerse', style=e, withlvl=False)
    del_lvl()