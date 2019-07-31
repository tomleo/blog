import os
import re
import codecs


def mkdirp(dir_path) -> None:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def slugify(string) -> str:
    _string = string
    unicode_quote_chars = [
        '„',
        '‚',
        '“',
        '‟',
        '‘',
        '‛',
        '”',
        '’',
        '"',
        '❛',
        '❜',
        '❟',
        '❝',
        '❞',
        '❮',
        '❯',
        '⹂',
        '〝',
        '〞',
        '〟',
        '＂',
        '«',
        '‹',
        '»',
        '›',
    ]
    for char in unicode_quote_chars:
        _string = re.sub(char, '', _string)
    _string = re.sub(r',|\:|\?|\(|\)|\'|\!|<|>', '', _string)

    _string = re.sub(r'&', 'and', _string)
    _string = re.sub(r'%', 'percent', _string)

    # Unicode small space is not visible, and odd with monotype editor fonts
    # so its encoded in bytes for the sake of making sense of this following line
    unicode_small_space = codecs.decode(b'\xe2\x80\x8a', 'utf-8')
    unicode_dash_chars = [
        '—',
        '‒',
        '–',
        '⁓',
        '┄',
        '﹉',
        '╍',
        '﹍',
        '┅',
        '┈',
        '┉',
        '┉',
        '┉',
        unicode_small_space,
    ]
    _string = re.sub(r'\ |\/', '-', _string)
    for char in unicode_dash_chars:
        _string = re.sub(char, '-', _string)

    if _string.endswith('.'):
        _string = _string[:-1]
    return _string.lower()
