import codecs
from luadata.serializer.unserialize import unserialize


def read(path, encoding="utf-8"):
    """Read luadata from file

    Args:
        path (str): file path
        encoding (str, optional): file encoding. Defaults to "utf-8".

    Returns:
        tuple([*]): unserialized data from luadata file
    """
    with codecs.open(path, "r", encoding) as file:
        return unserialize(file.read())
