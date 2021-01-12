def encode(plain, encoding):
    """WString Encode

    Args:
        plain (string): plain string
        encoding (string): target encoding

    Returns:
        string: encoded string
    """
    wstr = ""
    for char in plain:
        byte = char.encode(encoding)
        if len(byte) > 1:
            byte = (
                byte.replace(b"\\", b"\\\\")
                .replace(b'"', b'\\"')
                .replace(b"\n", b"\\\n")
            )
        wstr = wstr + byte.decode(encoding)
    return wstr
