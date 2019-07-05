import codecs
import numbers


def format_space(depth, fl):
    for i in range(0, depth):
        fl.write('\t')


def write_list(depth, lists, fl):
    fl.write('{\n')
    for i, val in enumerate(lists):
        format_space(depth + 1, fl)
        write_item(depth + 1, val, fl)
        fl.write(',\n')
    format_space(depth, fl)
    fl.write('}')


def write_dict(depth, dic, fl):
    no_hash = True
    last_key = None
    fl.write('{\n')
    for key, val in dic.items():
        if val is None:
            continue
        format_space(depth + 1, fl)
        if no_hash and (
            not isinstance(key, (int, float))
            or (last_key is None and key != 1)
            or (last_key is not None and last_key + 1 != key)
        ):
            no_hash = False
        if not no_hash:
            if isinstance(key, str):
                fl.write('%s = ' % key)
            else:
                fl.write('[%s] = ' % str(key))
        write_item(depth + 1, val, fl)
        fl.write(',\n')
        last_key = key
    format_space(depth, fl)
    fl.write('}')


def write_item(depth, item, fl):
    if isinstance(item, float):
        fl.write(item)
    elif isinstance(item, int):
        fl.write(item)
    elif isinstance(item, numbers.Integral):
        fl.write(item)
    elif isinstance(item, bool):
        fl.write('true' if item else 'false')
    elif isinstance(item, str):
        fl.write('\"%s\"' % item)
    elif isinstance(item, dict):
        write_dict(depth, item, fl)
    elif isinstance(item, list):
        write_list(depth, item, fl)


def serialize(data, path, encoding='utf-8'):
    fl = codecs.open(path, 'w', encoding)
    fl.write('data = ')
    write_item(0, data, fl)
    fl.close()
