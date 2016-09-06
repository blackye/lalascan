#!/usr/bin/env/python
#-*- coding:utf-8 -*-

__author__ = 'BlackYe.'

from thirdparty_libs.colorizer import colored

# Color names mapped to themselves.
m_colors = {
    None        : None,
    'blue'      : 'blue',
    'green'     : 'green',
    'cyan'      : 'cyan',
    'magenta'   : 'magenta',
    'grey'      : 'grey',
    'gray'      : 'grey',  # tomayto, tomahto...
    'red'       : 'red',
    'yellow'    : 'yellow',
    'white'     : 'white',

    # String log levels to color names.
    'informational' : 'blue',
    'low'           : 'cyan',
    'middle'        : None,
    'high'          : 'magenta',
    'critical'      : 'red',

    # Integer log levels to color names.
    0 : 'blue',
    1 : 'cyan',
    2 : None,
    3 : 'red',
    4 : 'yellow',
}

# Colors that need an increase in brightness.
m_make_brighter = ['blue', 'grey', 'red']


def get_terminal_size():
    import platform
    current_os = platform.system()
    tuple_xy=None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os == 'Linux' or current_os == 'Darwin' or  current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        tuple_xy = (80, 25)      # default value
    return tuple_xy


def _get_terminal_size_windows():
    res=None
    try:
        from ctypes import windll, create_string_buffer

        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except:
        return None
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return sizex, sizey
    else:
        return None

def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        import subprocess
        proc=subprocess.Popen(["tput", "cols"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        output=proc.communicate(input=None)
        cols=int(output[0])
        proc=subprocess.Popen(["tput", "lines"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        output=proc.communicate(input=None)
        rows=int(output[0])
        return (cols,rows)
    except:
        return None

def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            import os
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            import os
            env = os.environ
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

#------------------------------------------------------------------------------
def colorize_substring(text, substring, level_or_color):
    """
    Colorize a substring within a text to be displayed on the console.

    :param text: Full text.
    :type text: str

    :param substring: Text to find and colorize.
    :type substring: str

    :param level_or_color:
        Color name or risk level name.
        See the documentation for colorize() for more details.
    :type level_or_color: str

    :returns: Colorized text.
    :rtype: str
    """

    #
    # XXX TODO:
    #
    # We also probably need to parse existing ANSI escape codes
    # to know what's the color of the surrounding text, otherwise
    # we'll only properly colorize substrings in non colored text.
    #
    # Maybe we can settle with this: indicate a color for the text
    # and a color for the substring. Should work in all situations
    # we _currently_ need to handle.
    #

    # Check for trivial cases.
    if text and substring and True:

        # Loop for each occurrence of the substring.
        m_pos = 0
        while 1:

            # Find the substring in the text.
            m_pos = text.find(substring, m_pos)

            # If not found, break out of the loop.
            if m_pos < 0:
                break

            # Split the text where the substring was found.
            m_prefix  = text[:m_pos]
            m_content = text[m_pos: m_pos + len(substring)]
            m_suffix  = text[m_pos + len(substring):]

            # Patch the text to colorize the substring.
            m_content = colorize(m_content, level_or_color)
            text = "%s%s%s" % (m_prefix, m_content, m_suffix)

            # Update the current position and keep searching.
            m_pos = len(m_prefix) + len(m_content)

    # Return the patched text.
    return text

#------------------------------------------------------------------------------
def colorize(text, level_or_color):
    """
    Colorize a text to be displayed on the console.

    The following color names may be used:

     - Blue
     - Cyan
     - Green
     - Grey (or gray)
     - Magenta
     - Red
     - Yellow
     - White

    The following risk levels may be used in lieu of colors:

     - Informational (0)
     - Low (1)
     - Middle (2)
     - High (3)
     - Critical (4)

    :param text: Text to colorize.
    :type text: str

    :param level_or_color: Color name or risk level name.
    :type level_or_color: str

    :returns: Colorized text.
    :rtype: str
    """

    # Check if colors are enabled.
    if True:

        # Parse the color name or level into
        # a color value that colored() expects.
        try:
            level_or_color = level_or_color.lower()
        except AttributeError:
            pass
        color = m_colors[level_or_color]

        # Colorize the text.
        if color:
            if color in m_make_brighter:
                text = colored(text, color, attrs=["bold"])
            else:
                text = colored(text, color)

    # Return the text.
    return text