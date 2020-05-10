# luadata

This is a Python package that can serialize `Python` list &amp; dictionary to `Lua` table, or unserialize `Lua` table to `Python` list & dictionary.

## Install

Binary installers for the latest released version are available at the `Pypi`.
```
python -m pip install --upgrade luadata
```

## Use

You can use `write` to output your Python data into a Lua file on path.
```
luadata.write(data, path, encoding='utf-8', form=False, prefix='return ')
```
Or use `read` to input your Python data from a Lua file on path.
```
data = luadata.read(path, encoding='utf-8')
```
If only want to serialize or unserialize string data, You can try `serialize` and `unserialize`.
```
luadata.serialize(data, form=False)
luadata.unserialize(src_data)
```

## License

[BSD](https://github.com/leafvmaple/luadata/blob/master/LICENSE)