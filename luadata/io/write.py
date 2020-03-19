import codecs
import numbers


def concat(*args):
    sz = ''
    for arg in args:
        if type(arg) == str:
            sz += arg
    return sz


def check_list(dic):
    flag = {}
    count = 0
    for key, val in dic.items():
        if val is None:
            continue
        if not isinstance(key, (int, float)):
            return False
        flag[key] = True
        count += 1
    return len(flag) == count


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
        if self.form:
            return '%s = ' % key if isinstance(key, str) else '[%s] = ' % str(key)
        else:
            return '%s=' % key if isinstance(key, str) else '[%s]=' % str(key)

    def parse_list(self, lists, depth):
        sz = ''
        for i, val in enumerate(lists):
            sz = concat(sz, self.format_space(depth), self.parse_item(val, depth), ',', self.format_enter())
        return sz

    def parse_dict(self, dic, depth):
        sz = ''
        is_list = not check_list(dic)
        for key, val in dic.items():
            if val is None:
                continue
            sz = concat(sz, self.format_space(depth), self.format_key(key) if is_list else '',
                        self.parse_item(val, depth), ',', self.format_enter())
        return sz

    def parse_item(self, item, depth):
        if isinstance(item, float):
            return str(item)
        elif isinstance(item, int):
            return str(item)
        elif isinstance(item, numbers.Integral):
            return str(item)
        elif isinstance(item, bool):
            return 'true' if item else 'false'
        elif isinstance(item, str):
            return '\"%s\"' % item
        elif isinstance(item, dict):
            return concat('{', self.format_enter(), self.parse_dict(item, depth + 1), self.format_space(depth), '}')
        elif isinstance(item, list):
            return concat('{', self.format_enter(), self.parse_list(item, depth + 1), self.format_space(depth), '}')
        elif isinstance(item, const):
            return str(item)


def serialize(data, form=False):
    stream = StringStream(form)
    return stream.parse_item(data, 0)


def write(data, path, encoding='utf-8', form=False, prefix='return '):
    fl = codecs.open(path, 'w', encoding)
    sz = serialize(data, form).replace('\\t', '\t').replace('\\n', '\n')
    fl.write(prefix + sz)
    fl.close()
