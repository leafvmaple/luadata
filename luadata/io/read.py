import codecs


def read_seek(fl, offset):
    tell = fl.tell()
    fl.seek(tell + offset)


def read_trim(fl):
    while True:
        ch = fl.read(1)
        if ch != '\r' and ch != '\n' and ch != '\t' and ch != ' ':
            read_seek(fl, -1)
            break


def read_string(fl):
    buffer = ""

    read_trim(fl)
    while True:
        ch = fl.read(1)
        if ch == '\r' or ch == '\n' or ch == ' ' or ch == '{' or ch == '}' or ch == '=' or ch == ',':
            read_seek(fl, -1)
            return buffer
        else:
            buffer += ch


def read_key(fl):
    read_trim(fl)
    key = read_string(fl)
    read_trim(fl)
    str_len = len(key)
    if str_len > 0 and key[0] == '[' and key[str_len - 1] == ']':
        key = key[1:str_len - 1]

    if key.isdigit():
        return int(key)

    return key


def read_table(fl):
    index = 0
    table = {}

    while True:
        ch = fl.read(1)
        if ch == "}":
            break
        else:
            read_seek(fl, -1)

        key = read_key(fl)
        ch = fl.read(1)
        if ch == "=":
            table[key] = read_item(fl)
        else:
            read_seek(fl, -1)
            table[index] = key
            index += 1

        read_trim(fl)
        ch = fl.read(1)
        if ch == '}':
            break
        elif ch != ',':
            print('Get Table Error')
        read_trim(fl)

    return table


def read_item(fl):
    read_trim(fl)
    ch = fl.read(1)
    if ch == '{':
        return read_table(fl)

    read_seek(fl, -1)
    str = read_string(fl)
    if str.isdigit():
        return float(str)
    elif str == "true":
        return True
    elif str == 'false':
        return False
    else:
        return str


def unserialize(path, encoding='utf-8'):
    fl = codecs.open(path, 'r', encoding)
    data = read_table(fl)
    fl.close()
    return data

# unserialize('.\Test.lua')