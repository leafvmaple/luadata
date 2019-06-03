import codecs


class StreamData:
    def __init__(self, data, p):
        self.data = data
        self.p = p


def valid(ch):
    return ch != '\r' and ch != '\n' and ch != '\t' and ch != ' '


def format_marks(string):
    str_len = len(string)
    if str_len > 0 and string[0] == '\"' and string[str_len - 1] == '\"':
        return string[1:str_len - 1]
    elif str_len > 0 and string[0] == '\'' and string[str_len - 1] == '\'':
        return string[1:str_len - 1]
    return string


def format_value(val):
    if val.isdigit():
        return int(val)


def read_char(info):
    return info.data[info.p]


def read_next(info):
    info.p += 1
    return read_char(info)


def read_trim(info):
    ch = read_char(info)
    while not valid(ch):
        ch = read_next(info)


def read_chars(info):
    buffer = ""
    read_trim(info)
    ch = read_char(info)
    while valid(ch) and ch != '{' and ch != '}' and ch != '=' and ch != ',':
        buffer += ch
        ch = read_next(info)
    read_trim(info)
    return buffer


def read_brackets(info):
    buffer = ""
    read_trim(info)
    ch = read_next(info)
    while ch != ']':
        buffer += ch
        ch = read_next(info)
    info.p += 1
    read_trim(info)
    return buffer


def read_string(info):
    buffer = ""
    read_trim(info)
    left_ch = read_char(info)
    ch = read_next(info)
    while ch != left_ch:
        buffer += ch
        ch = read_next(info)
    info.p += 1
    read_trim(info)
    return buffer


def read_table(info):
    index = 0
    table = {}
    lists = []

    ch = read_next(info)
    while ch != '}':
        key = read_key(info)
        read_trim(info)
        ch = read_char(info)
        if ch == "=":
            info.p += 1
            table[key] = read_item(info)
        else:
            index += 1
            table[index] = format_value(key)

        read_trim(info)
        ch = read_char(info)

        if ch == ',':
            info.p += 1
            read_trim(info)
            ch = read_char(info)

    info.p += 1

    for i in range(1, len(table) + 1):
        if i in table:
            lists.append(table[i])

    if len(lists) == len(table):
        return lists
    return table


def read_key(info):
    read_trim(info)
    ch = read_char(info)
    if ch == '\"' or ch == '\'':
        return read_string(info)
    elif ch == '[':
        key = read_brackets(info)
        if key[0] == '\"' or key[0] == '\'':
            return format_marks(key)
        elif key.isdigit():
            return int(key)
        return key
    else:
        return read_chars(info)


def read_item(info):
    read_trim(info)
    ch = read_char(info)
    if ch == '{':
        return read_table(info)
    elif ch == '\"' or ch == '\'':
        return read_string(info)

    item = read_chars(info)
    if item.isdigit():
        return int(item)
    elif item == "true":
        return True
    elif item == 'false':
        return False
    else:
        return item


def unserialize(src, encoding='utf-8'):
    if isinstance(src, str):
        fl = codecs.open(src, 'r', encoding)
        src = fl.read()
    data = read_item(StreamData("{%s}" % src, 0))
    fl.close()
    return data
