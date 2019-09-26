import os
import re
import codecs

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
    # Unicode small space is not visible, and odd with monotype editor fonts
    # so its encoded in bytes for the sake of making sense of this following line
    codecs.decode(b'\xe2\x80\x8a', 'utf-8'),
]


def mkdirp(dir_path) -> None:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def slugify(string) -> str:
    _string = string
    for char in unicode_quote_chars:
        _string = re.sub(char, '', _string)
    _string = re.sub(r',|\:|\?|\(|\)|\'|\!|<|>', '', _string)

    _string = re.sub(r'&', 'and', _string)
    _string = re.sub(r'%', 'percent', _string)
    _string = re.sub(r'\ |\/', '-', _string)
    for char in unicode_dash_chars:
        _string = re.sub(char, '-', _string)

    if _string.endswith('.'):
        _string = _string[:-1]
    return _string.lower()
