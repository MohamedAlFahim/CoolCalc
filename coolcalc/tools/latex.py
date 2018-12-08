def underline(content):
    return '\\underline{' + content + '}'


def bold(content):
    return '\\textbf{' + content + '}'


def italic(content):
    return '\\textit{' + content + '}'


def text(content):
    return '\\text{' + content + '}'


def color(color_name, content):
    return f'\\color{{{color_name}}}{{{content}}}'


def convert_rgb_to_hex(red, green, blue):
    return f'#{red:02x}{green:02x}{blue:02x}'
