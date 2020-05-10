import codecs
import numbers
import re

def concat(*args):
    sz = ''
    for arg in args:
        if type(arg) == str:
            sz += arg
    return sz


def check_list(key, last_key):
    if not isinstance(key, int):
        return False
    if last_key is None and key != 1:
        return False
    if last_key is not None and last_key + 1 != key:
        return False
    return True

class const:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data


class StringStream:
    def __init__(self, form):
        self.form = form

    def format_space(self, depth):
        return concat(*['\\t' for i in range(depth)]) if self.form else ''

    def format_enter(self):
        return '\\n' if self.form else ''

    def format_key(self, key):
        if isinstance(key, str):
            return key if len(re.findall("^[a-zA-Z_][a-zA-Z0-9_]*$", key)) > 0 else '["%s"]' % key
        else:
            return "[%s]" % str(key)

    def format_keyvalue(self, key, val, depth):
        return ('%s = %s' if self.form else '%s=%s') % (self.format_key(key), self.parse_item(val, depth))

    def parse_list(self, lists, depth):
        sz = ''
        is_first = True
        for i, val in enumerate(lists):
            split_text = '' if is_first else ','
            sz = concat(sz, split_text, self.format_enter(), self.format_space(depth), self.parse_item(val, depth))
            is_first = False
        return sz

    def parse_dict(self, dic, depth):
        sz = ''
        is_list = True
        last_key = None
        is_first = True
        for key, val in dic.items():
            if val is None:
                continue
            is_list = True if is_list and check_list(key, last_key) else False

            split_text = '' if is_first else ','
            item_text = self.format_keyvalue(key, val, depth) if not is_list else self.parse_item(val, depth)

            sz = concat(sz, split_text, self.format_enter(), self.format_space(depth), item_text)

            last_key = key
            is_first = False
        return sz

    def parse_item(self, item, depth):
        if isinstance(item, bool):
            return 'true' if item else 'false'
        elif isinstance(item, float):
            return str(item)
        elif isinstance(item, int):
            return str(item)
        elif isinstance(item, numbers.Integral):
            return str(item)
        elif isinstance(item, str):
            return '\"%s\"' % item
        elif isinstance(item, dict):
            return concat('{', self.parse_dict(item, depth + 1), self.format_enter(), self.format_space(depth), '}')
        elif isinstance(item, list):
            return concat('{', self.parse_list(item, depth + 1), self.format_enter(), self.format_space(depth), '}')
        elif isinstance(item, const):
            return str(item)


def format_string(s, encoding):
    if encoding != 'utf-8':
        res = ''
        for ch in s:
            byte = ch.encode(encoding)
            if len(byte) > 1:
                byte = byte.replace(b'\\', b'\\\\').replace(b'\"', b'\\\"').replace(b'\"', b'\\\n')
            res = res + byte.decode(encoding)
        return res
    return s

def serialize(data, form=False):
    stream = StringStream(form)
    return stream.parse_item(data, 0)

def write(data, path, encoding='utf-8', form=False, prefix='return '):
    fl = codecs.open(path, 'w', encoding)
    sz = serialize(data, form).replace('\\t', '\t').replace('\\n', '\n')
    fl.write(format_string(prefix + sz, encoding))
    fl.close()