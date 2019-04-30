import os, codecs, numbers

def format_space(depth, fl):
    for i in range(0, depth):
        fl.write('\t')

def write_list(depth, list, fl):
    fl.write('{\n')
    for i, val in enumerate(list):
        format_space(depth + 1, fl)
        write_item(depth + 1, val, fl)
        fl.write(',\n')
    format_space(depth, fl)
    fl.write('}')

def write_dict(depth, dic, fl):
    nohash = True
    lastkey = None
    fl.write('{\n')
    for key, val in dic.items():
        if val is None:
            continue
        format_space(depth + 1, fl)
        if nohash and (
            not isinstance(key, (int, float))
            or (lastkey is None and key != 1)
            or (lastkey is not None and lastkey + 1 != key)):
            nohash = False
        if not nohash:
            if isinstance(key, str):
                fl.write('%s = ' % key)
            else:
                fl.write('[%s] = ' % str(key))
        write_item(depth + 1, val, fl)
        fl.write(',\n')
        lastkey = key
    format_space(depth, fl)
    fl.write('}')

def write_item(depth, item, fl):
    if isinstance(item, float):
        fl.write('%f' % item)
    elif isinstance(item, int):
        fl.write('%d' % item)
    elif isinstance(item, str):
        fl.write('\"%s\"' % item)
    elif isinstance(item, dict):
        write_dict(depth, item, fl)
    elif isinstance(item, list):
        write_list(depth, item, fl)

def serialize(data, dstpath, encoding='utf-8'):
    fl = codecs.open(dstpath, 'w', encoding)
    fl.write('data = ')
    write_item(0, data, fl)
    fl.close()