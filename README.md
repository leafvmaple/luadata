# Luadata

This is a Python package that serialized `Python` list &amp; dictionary to `Lua` table.

## Install

Binary installers for the latest released version are available at the `Pypi`.
```
python -m pip install --upgrade luadata
```

## Use

You can use `serialized` to output your Python data into a Lua file on dstpath.
```
luadata.serialized(data, dstpath, encoding='utf-8')
```

## License

[BSD](https://github.com/leafvmaple/luadata/blob/master/LICENSE)