# luadata

This is a Python package that can serialize `Python` list &amp; dictionary to `Lua` table, or unserialize `Lua` table to `Python` list & dictionary.

## Install

Binary installers for the latest released version are available at the `Pypi`.
```
python -m pip install --upgrade luadata
```

## Use

You can use `serialize` to output your Python data into a Lua file on path.
```
luadata.serialize(data, path, encoding='utf-8')
```
Or use `unserialize` to input your Python data from a Lua file on path.
```
data = luadata.unserialize(path, encoding='utf-8')
```

## License

[BSD](https://github.com/leafvmaple/luadata/blob/master/LICENSE)