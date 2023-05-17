"""
This module provides a collection of functions for working with the console.

Functions:
- init(...): Initializes the console configuration.
- clear_screen(): Clears the console screen.
- add_lvl(): Adds a new level to the console.
- del_lvl(): Deletes the last added level from the console.
- println(...): Prints a message to the console.
- inputln(...): Prints a message to the console and returns the user input.
- start_block(...): Starts a new message block with a given color and background color.
- end_block(...): Ends the current message block and prints a message.
- warning(...): Prints a warning message to the console.
- error(...): Prints an error message to the console.
- new_line(): Prints a new line to the console.
- line(...): Prints a horizontal line to the console.
- print_emoji_list(): Prints a list of supported emojis to the console.
- print_color_list(): Prints a list of supported colors to the console.
- print_style_list(): Prints a list of supported text styles to the console.
- print_matrix(...): Prints a matrix to the console.
- textbox(...): Prints a textbox to the console.

Constants:
- NAME: The name of the module.

Decorators:
- block(...): Decorator to create a block of text.

Notes:
- The console is managed by the Console class.
- The console configuration is managed by the Config class.
- The console colors are managed by the ColorText and ColorBackground classes.
- The console text styles are managed by the StyleText class.
- The console emojis are managed by the Emoji class.
- The console exceptions are managed by the exceptions module.
"""


from typing import (
    Any,
    List,
    Union,
    Callable
)
import functools
import os

from consoleverse.config import lang
from consoleverse.term import *
from consoleverse.exceptions import *


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          constants                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
NAME : str = 'ConsoleVerse'

__START_LANGS = {
    lang.Language()['en'] : 'START',
    lang.Language()['es'] : 'INICIA',
}

__END_LANGS = {
    lang.Language()['en'] : 'END',
    lang.Language()['es'] : 'TERMINA',
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                         decorators                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def block(message_block: Union[str, dict],
          text_color: str = 'BLUE',
          bg_color: str = ''
          ) -> Callable[..., Any]:
    """
    Decorator to create a block of text.

    Parameters
    ----------
    message_block : Union[str, dict]
        if is a str, then is the title of the block, if is a dict, then is the
        title is taken according to the language selected in the config file,
        e.g. {'en': 'Title', 'es': 'Título'} the title is printed is Title if the
        language is `en`, and Título if the language is `es`.

    text_color : str, optional
        The color of the message, by default BLUE

    bg_color : str, optional
        The background color of the message, by default has no color
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            message = message_block
            if isinstance(message_block, dict):
                message = message_block[lang.lang()]

            start_block(message, color=text_color, bg_color=bg_color)
            new_line()
            value = func(*args, **kwargs)
            new_line()
            end_block(message, color=text_color, bg_color=bg_color)
            return value
        return wrapped
    return decorator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          functions                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class _ConsoleConfig:
    _indentation_type  : str = ' '
    _indentation_lvl   : str = ''
    _indentantion_size : int = 2
    _is_init : bool = False
    _autoreset_colors: bool = True

    @staticmethod
    def init(clear: bool = True,
             indentation_type: str = ' ',
             indentation_size: int = 2,
             autoreset_colors: bool = True
             ):
        """
        Initialize the console, and resert the indentation level

        Parameters
        ----------
        clear : bool, optional
            True to clear the screen and False is not, by default True
        """
        _ConsoleConfig._indentation_lvl = ''
        _ConsoleConfig._indentantion_size = indentation_size
        _ConsoleConfig._indentation_type  = indentation_type
        _ConsoleConfig._autoreset_colors  = autoreset_colors

        if clear:
            clear_screen()
        _ConsoleConfig._is_init = True

    @staticmethod
    def reset_config() -> None:
        _ConsoleConfig._indentation_type  : str = ' '
        _ConsoleConfig._indentation_lvl   : str = ''
        _ConsoleConfig._indentantion_size : int = 2
        _ConsoleConfig._is_init : bool = False
        _ConsoleConfig._autoreset_colors : bool = True

    @staticmethod
    def _init():
        """
        If the console still doesn't start, then start the console without
        indentation.
        """
        if not _ConsoleConfig._is_init:
            _ConsoleConfig._is_init = True
            _ConsoleConfig._indentation_lvl = ''

    @staticmethod
    def indentation_lvl() -> str:
        return _ConsoleConfig._indentation_lvl

    @staticmethod
    def add_indentation_lvl() -> None:
        _ConsoleConfig._indentation_lvl += (_ConsoleConfig._indentation_type * _ConsoleConfig._indentantion_size)

    @staticmethod
    def del_indentation_lvl() -> None:
        _ConsoleConfig._indentation_lvl = _ConsoleConfig._indentation_lvl[:-_ConsoleConfig._indentantion_size]


def init(clear: bool = True,
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
    _ConsoleConfig.init(
        clear=clear,
        indentation_type=indentation_type,
        indentation_size=indentation_size,
        autoreset_colors=autoreset_colors
    )

    if clear:
        clear_screen()
    _ConsoleConfig._is_init = True


def reset_colors() -> None:
    """
    Reset the colors of the console
    """
    print(ColorText().reset(), end='')


def reset_config() -> None:
    """
    Reset the configuration of the console
    """
    _ConsoleConfig.reset_config()


def clear_screen():
    """
    Clear the console screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def add_lvl():
    """
    Add one level (indentation)
    """
    _ConsoleConfig.add_indentation_lvl()


def del_lvl():
    """
    Substract one level (indentation)
    """
    _ConsoleConfig.del_indentation_lvl()


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
    ctext = ColorText()
    ctext = ctext[color] if color in ctext else ''
    cbaground = ColorBackground()
    cbaground = cbaground[bg_color] if bg_color in cbaground else ''
    stext = StyleText()
    stext = stext[style] if style in stext else ''
    colorized_text = f'{ctext}{cbaground}{stext}{text}'

    if reset_console_colors:
        colorized_text += ColorText().reset()

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
    _ConsoleConfig._init()
    message = __to_string(*message, sep=sep)

    if withlvl:
        message = _ConsoleConfig._indentation_lvl + message

    colorized_text: str = _colorize(text=message,
                                    color=color,
                                    bg_color=bg_color,
                                    style=style,
                                    reset_console_colors=reset_all_colors
                                    )
    print(colorized_text, end=endl)


def __to_string(*values: Any, sep: str = ' ') -> str:
    return sep.join([str(m) for m in values])


def start_block(*message: Any, color: str = 'BLUE', bg_color: str = '') -> None:
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
    println(f'{__START_LANGS[lang.lang()]} {message.upper()}',
            color=color,
            bg_color=bg_color
            )
    add_lvl()


def end_block(*message: Any,
              color: str = 'BLUE',
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
    println(f'{__END_LANGS[lang.lang()]} {message.upper()}',
            color=color,
            bg_color=bg_color,
            style=style
            )
    new_line()


def warning(*message: Any,
            color: str = 'BLUE',
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
          color: str = 'RED',
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


def __max_len_value(matrix, nan_format) -> int:
    """
    The function calculates the maximum length of a value in a matrix, replacing NaN values with a
    specified format.

    Parameters
    ----------
    matrix : List[List[Any]]
        a 2D matrix (list of lists) containing values to be checked for maximum length

    nan_format : str
        The string format to use when a cell in the matrix is a NaN value

    Returns
    -------
    int
        an integer value which represents the maximum length of a value in a given matrix.
    """

    def max_value(cell) -> int:
        cellstr = str(cell)
        if cellstr in ('None', 'nan', 'NaN'):
            cellstr = nan_format
        return max(max_len, len(cellstr))

    max_len = 0
    for row in matrix:
        if isinstance(row, list):
            for col in row:
                max_len = max_value(col)
        else:
            max_len = max_value(row)
    return max_len


def __print_matrix_header(header: List[str],
                          len_index: int,
                          color_index: str,
                          extra_spacing: str,
                          withlvl: bool,
                          max_len_value: int,
                          lvl_space: int = 3
                          ) -> None:
    """
    Print the header of the matrix

    Parameters
    ----------
    header : List[str]
        If the matrix has a header to print with them, by default None

    len_index : int
        Longest value size index of the indexes

    color_index : str
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available

    extra_spacing : str
        The extra spacing befote printing the header

    withlvl : bool
        True if the matrix should be printed with the current indentation False in otherwise

    max_len_value : int
        Longest value size in the matrix

    lvl_space : int
        Number of aditional spaces based on the style
    """
    spaces: str = ' ' * (len_index + lvl_space)
    indentation: str = _ConsoleConfig._indentation_lvl if withlvl else ''

    println(f'{indentation}{spaces}{extra_spacing}', endl='', withlvl=False)
    for h in header:
        println(f' {h : ^{max_len_value}} ', color=color_index, endl='', withlvl=False)
    new_line()


def __print_matrix_row(row: list,
                       max_len_value: int,
                       color: str,
                       nan_format: str,
                       color_style: str,
                       color_index: str,
                       end_line: str,
                       start_line: str,
                       index_name: str,
                       indentation: str
                       ) -> None:
    """
    Printed the row of the matrix.

    Parameters
    ----------
    row : list
        The row of the matrix to be printed

    max_len_value : int
        Longest value size in the matrix

    color : str
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available

    nan_format : str
        The formatted string to print a NaN/None value

    color_style : str
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available

    color_index : str
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available

    end_line : str
        The end of line to be printed

    start_line : str
        The beginning of line to be printed

    index_name : str
        The name of the index to be printed

    indentation : str
        The indentation of the line
    """
    println(indentation, endl='', withlvl=False)
    println(index_name,  endl='', color=color_index, withlvl=False)
    println(start_line,  endl='', color=color_style, withlvl=False)

    for cell in row:
        cellstr = str(cell) if str(cell) not in ('None', 'nan', 'NaN', '') else nan_format
        println(f' {cellstr : ^{max_len_value}} ', color=color, endl='', withlvl=False)
    println(end_line, color=color_style, withlvl=False)


def __print_matrix_base(matrix,
                        header: List[str],
                        indexes: Union[List[str], str],
                        nan_format: str,
                        color: str,
                        color_index: str,
                        color_style: str,
                        max_len_value: int,
                        len_index: int,
                        style : str,
                        withlvl: bool,
                        start_line: str,
                        end_line: str,
                        top_line: str,
                        bottom_line: str,
                        middle_vertical_line: str,
                        middle_horizontal_line: str,
                        level_space: int = 3
                        ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise

    start_line : str
        The beginning of line to be printed

    end_line : str
        The end of line to be printed

    top_line : str, optional
        The top line of the matrix

    bottom_line : str, optional
        The bottom line of the matrix

    middle_vertical_line : str, optional
        The middle vertical line of the matrix

    middle_horizontal_line : str, optional
        The middle horizontal line of the matrix

    level_space : int, optional
        The space between the level and the matrix, by default 3
    """
    indentation: str = _ConsoleConfig._indentation_lvl if withlvl else ''

    if header:
        __print_matrix_header(header=header,
                              len_index=len_index,
                              color_index=color_index,
                              extra_spacing='',
                              withlvl=withlvl,
                              max_len_value=max_len_value,
                              lvl_space=level_space
                              )

    if top_line is not None and top_line != '':
        println(top_line, color=color_style, withlvl=False)

    for index_row_id, row in enumerate(matrix):
        __print_matrix_row(row = row,
                           max_len_value = max_len_value,
                           color = color,
                           nan_format = nan_format,
                           color_style = color_style,
                           color_index = color_index,
                           end_line = end_line,
                           start_line = start_line,
                           index_name = f'{indexes[index_row_id]: >{len_index}}' if indexes is not None else '',
                           indentation = indentation
                           )

    if bottom_line is not None and bottom_line != '':
        println(bottom_line, color=color_style, withlvl=False)


def __print_matrix_box_style(matrix,
                             header: List[str],
                             indexes: Union[List[str], str],
                             nan_format: str,
                             color: str,
                             color_index: str,
                             color_style: str,
                             max_len_value: int,
                             len_index: int,
                             style : str,
                             withlvl: bool
                             ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    div: str = '-' * (len(matrix[0]) * max_len_value) + '-' * (len(matrix[0]) * 2)
    spaces: str = ' ' * (len_index + 3)
    indentation: str = _ConsoleConfig._indentation_lvl if withlvl else ''

    __print_matrix_base(matrix=matrix,
                        header=header,
                        indexes=indexes,
                        nan_format=nan_format,
                        color=color,
                        color_index=color_index,
                        color_style=color_style,
                        max_len_value=max_len_value,
                        len_index=len_index,
                        style=style,
                        withlvl=withlvl,
                        start_line=' | ',
                        end_line=f' | ' if style == 'box' else '',
                        top_line=f'{indentation}{spaces}{div}',
                        bottom_line=f'{indentation}{spaces}{div}' if style == 'box' else new_line(),
                        middle_vertical_line=None,
                        middle_horizontal_line=None
                        )


def __print_matrix_numpy_style(matrix,
                               header: List[str],
                               indexes: Union[List[str], str],
                               style: str,
                               nan_format: str,
                               color: str,
                               color_index: str,
                               color_style: str,
                               max_len_value: int,
                               len_index: int,
                               withlvl: bool
                               ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    indentation: str = _ConsoleConfig._indentation_lvl if withlvl else ''

    if header is not None:
        __print_matrix_header(header = header,
                              len_index = len_index,
                              color_index = color_index,
                              extra_spacing = '   ',
                              withlvl = withlvl,
                              max_len_value = max_len_value
                              )

    max_rows: int = len(matrix)

    for index_row_id, row in enumerate(matrix):
        # string line
        if index_row_id == 0:
            println(indentation, '[ ', endl='', color=color_style, withlvl=False)
        else:
            println('  ', indentation, endl='', withlvl=False)

        __print_matrix_row(row = row,
                           max_len_value = max_len_value,
                           color = color,
                           nan_format = nan_format,
                           color_style = color_style,
                           color_index = color_index,
                           end_line = ' ]' if max_rows != index_row_id + 1 else ' ]  ]',
                           start_line = ' [ ',
                           index_name = f'{indexes[index_row_id]: >{len_index}}' if indexes is not None else '',
                           indentation = indentation
                           )


def __print_matrix_without_style(matrix,
                                 header: List[str],
                                 indexes: Union[List[str], str],
                                 style: str,
                                 nan_format: str,
                                 color: str,
                                 color_index: str,
                                 color_style: str,
                                 max_len_value: int,
                                 len_index: int,
                                 withlvl: bool
                                 ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    __print_matrix_base(matrix=matrix,
                        header=header,
                        indexes=indexes,
                        nan_format=nan_format,
                        color=color,
                        color_index=color_index,
                        color_style=color_style,
                        max_len_value=max_len_value,
                        len_index=len_index,
                        style=style,
                        withlvl=withlvl,
                        start_line='',
                        end_line='',
                        top_line='',
                        bottom_line='',
                        middle_vertical_line=None,
                        middle_horizontal_line=None,
                        level_space=0
                        )


def __print_matrix_simpleline_style(matrix,
                                    header: List[str],
                                    indexes: Union[List[str], str],
                                    nan_format: str,
                                    color: str,
                                    color_index: str,
                                    color_style: str,
                                    max_len_value: int,
                                    len_index: int,
                                    style : str,
                                    withlvl: bool
                                    ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    div: str = Line.SH * (len(matrix[0]) * max_len_value + len(matrix[0]) * 2 + 2)
    spaces: str = ' ' * (len_index + 1)
    indentation: str = _ConsoleConfig._indentation_lvl if withlvl else ''

    __print_matrix_base(matrix=matrix,
                        header=header,
                        indexes=indexes,
                        nan_format=nan_format,
                        color=color,
                        color_index=color_index,
                        color_style=color_style,
                        max_len_value=max_len_value,
                        len_index=len_index,
                        style=style,
                        withlvl=withlvl,
                        start_line=f' {Line.SV} ',
                        end_line=f' {Line.SV} ',
                        top_line=f'{indentation}{spaces}{Line.STL}{div}{Line.STR}',
                        bottom_line=f'{indentation}{spaces}{Line.SBL}{div}{Line.SBR}',
                        middle_vertical_line=None,
                        middle_horizontal_line=None
                        )


def __print_matrix_doubleline_style(matrix,
                                    header: List[str],
                                    indexes: Union[List[str], str],
                                    nan_format: str,
                                    color: str,
                                    color_index: str,
                                    color_style: str,
                                    max_len_value: int,
                                    len_index: int,
                                    style : str,
                                    withlvl: bool
                                    ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    div: str = Line.DH * (len(matrix[0]) * max_len_value + len(matrix[0]) * 2 + 2)
    spaces: str = ' ' * (len_index + 1)
    indentation: str = _ConsoleConfig._indentation_lvl if withlvl else ''

    __print_matrix_base(matrix=matrix,
                        header=header,
                        indexes=indexes,
                        nan_format=nan_format,
                        color=color,
                        color_index=color_index,
                        color_style=color_style,
                        max_len_value=max_len_value,
                        len_index=len_index,
                        style=style,
                        withlvl=withlvl,
                        start_line=f' {Line.DV} ',
                        end_line=f' {Line.DV} ',
                        top_line=f'{indentation}{spaces}{Line.DTL}{div}{Line.DTR}',
                        bottom_line=f'{indentation}{spaces}{Line.DBL}{div}{Line.DBR}',
                        middle_vertical_line=None,
                        middle_horizontal_line=None
                        )


def print_matrix(matrix,
                 header: Union[List[str], str] = 'all',
                 indexes: Union[List[str], str] = 'all',
                 style: str = 'box',
                 nan_format: str = '',
                 color: str = None,
                 color_index: str = '',
                 color_style: str = '',
                 withlvl: bool = True
                 ) -> None:
    """
    Print a matrix in a pretty formatted

    >>> matrix = [[1, 2, 3], [4, 5, 6]]
    >>> print_matrix(matrix)
    ...
    ...     0  1  2
    ...     -------
    ... 0 | 1  2  3 |
    ... 1 | 4  5  6 |
    ...     -------

    >>> print_matrix(matrix,
    >>>              header=['one', 'two', 'three'],
    >>>              indexes=['row1', 'row2'],
    >>>              style='semibox'
    >>>              )
    ...
    ...          one     two    three
    ...        -----------------------
    ... row1 |    1       2       3
    ... row2 |    4       5       6

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str] | str, optional
        A list of strings if is a presonalized column name
        - `all` to show the index of the column,
        - `None` do not show any index, by default `all`

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name
        - `all` to show the index of the row,
        - `None` do not show any index, by default `all`

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix
        - `numpy` or `np` Has been printed like a NumPy matrix
        - `simpleline` or `line` or `sl` Only the grid lines of the matrix based on single lines of
           term.emojis.Line
        - `doubleline` or `dl` Only the grid lines of the matrix based on double lines of
           term.emojis.Line
        - `None` Without borders, only show the values

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `COLORS_LIST`
        ['RED', 'GREEN', ...], `console.COLORS_LIST` for all colors available;
        by default has no color

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    if indexes == 'all':
        indexes = [str(i) for i in range(len(matrix))]

    if header == 'all':
        header = [str(i) for i in range(len(matrix[0]))]


    max_len_value = __max_len_value(matrix, nan_format)
    max_len_value = max(max_len_value, __max_len_value([] if header is None else header, nan_format))

    len_index = 0

    if isinstance(indexes, list):
        len_index: int = __max_len_value(indexes, nan_format)

    kwargs = {'matrix' : matrix,
              'header' : header,
              'indexes' : indexes,
              'nan_format' : nan_format,
              'color' : color,
              'color_index' : color_index,
              'color_style' : color_style,
              'max_len_value' : max_len_value,
              'len_index' : len_index,
              'style' : style,
              'withlvl' : withlvl
              }

    if style is None:
        __print_matrix_without_style(**kwargs)
    elif style in ('box', 'semibox'):
        __print_matrix_box_style(**kwargs)
    elif style in ('numpy', 'np'):
        __print_matrix_numpy_style(**kwargs)
    elif style in ('simpleline', 'sl', 'line'):
        __print_matrix_simpleline_style(**kwargs)
    elif style in ('doubleline', 'dl'):
        __print_matrix_doubleline_style(**kwargs)
    else:
        # TODO: language support
        raise ErrorNotDefinedStyle(f'Unknown style: {style}')


def inputln(*message: Any,
            endl: str = '',
            input_type: type = str,
            withlvl: bool = True,
            color: str = '',
            bg_color: str = '',
            reset_all_colors: bool = True,
            style: str = '',
            sep: str = ' '
            ) -> None:
    """
    A utility function that prompts the user to input data from the console,
    with support for customization of the prompt message appearance.


    Parameters
    ----------
    message : Any
        Message to print to console

    endl : str, optional
        The end of the message, by default is empty

    input_type : type, optional
        The type of the input, by default `str`. This parameter specifies
        the type of the returned user input value.

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
    println(
        *message,
        endl=endl,
        withlvl=withlvl,
        color=color,
        bg_color=bg_color,
        reset_all_colors=reset_all_colors,
        style=style,
        sep=sep
    )

    return input_type(input())


# TODO: docstring
# TODO: add support for the personalized border style
# TODO: add support text alignment
def textbox(*message: Any,
            withlvl: bool = True,
            color: str = '',
            bg_color: str = '',
            reset_all_colors: bool = True,
            style: str = '',
            sep: str = ' ',
            border: str = 'simpleline',
            border_color: str = '',
            border_style: str = '',
            ) -> None:
    """
    Print the message to the console, the `endl` is the same as `end` in print function
    and is necessary print the message with the current indentation level and the color
    indicate.

    Parameters
    ----------
    message : Any
        Message to print to console

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

    border : str, optional
        The style of the border, the style must be one of the `STYLES_LIST`,
        by default is `simpleline`
    """
    message = __to_string(*message, sep=sep)
    lines = message.split('\n')

    max_len = max([len(line) for line in lines])

    if border == 'simpleline':
        top = Line.STL + Line.SH * (max_len + 2) + Line.STR
        bottom = Line.SBL + Line.SH * (max_len + 2) + Line.SBR
        vertical_blank = Line.SV + ' ' * (max_len + 2) + Line.SV
        vertical = Line.SV
    elif border == 'doubleline':
        top = Line.DTL + Line.DH * (max_len + 2) + Line.DTR
        bottom = Line.DBL + Line.DH * (max_len + 2) + Line.DBR
        vertical_blank = Line.DV + ' ' * (max_len + 2) + Line.DV
        vertical = Line.DV
    else:
        # TODO: language support
        raise ErrorNotDefinedStyle(f'Unknown border style: {border}')

    pln = lambda s: println(s, withlvl=withlvl, color=border_color, style=border_style)

    pln(top)
    pln(vertical_blank)

    for line in lines:
        println(vertical, withlvl=withlvl, color=border_color, style=border_style, endl='')
        println(
            ' ' + line + ' ',
            withlvl=False,
            color=color,
            bg_color=bg_color,
            reset_all_colors=reset_all_colors,
            style=style,
            endl=''
        )
        println(' ' * (max_len - len(line)), withlvl=False, endl='')
        println(vertical, withlvl=False, color=border_color, style=border_style)

    pln(vertical_blank)
    pln(bottom)

def progress_bar(progress: float,
                 width: int = 50,
                 bar: str = '#',
                 start_bar: str = '[',
                 end_bar: str = ']',
                 spacing: str = '.',
                 pct: bool = True,
                 **kwargs
                 ) -> None:
    """
    Print a progress bar to the console.

    Parameters
    ----------
    progress : float
        The progress of the bar, the value must be between 0 and 1

    width : int, optional
        The width of the bar, by default is 50

    bar : str, optional
        The character to use for the bar, by default is `#`

    start_bar : str, optional
        The character to use for the start of the bar, by default is `[`

    end_bar : str, optional
        The character to use for the end of the bar, by default is `]`

    spacing : str, optional
        The character to use for the spacing, by default is `.`

    pct : bool, optional
        True to print the percentage, False otherwise, by default is `True`
    """

    if progress < 0 or progress > 1:
        raise ValueError('The progress must be between 0 and 1')

    if width < 0:
        raise ValueError('The width must be greater than 0')

    if len(bar) != 1:
        raise ValueError('The bar must be a single character')

    if len(start_bar) != 1:
        raise ValueError('The start_bar must be a single character')

    if len(end_bar) != 1:
        raise ValueError('The end_bar must be a single character')

    progress_bar = int(progress * width)
    pct_bar = ' (' + str(int(progress * 100)) + '%)' if pct else ''

    println(
        start_bar + bar * progress_bar + spacing * (width - progress_bar) + end_bar + pct_bar,
        **kwargs
    )

