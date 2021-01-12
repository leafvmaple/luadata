def decode(wstr, encoding):
    """WString Decode

    Args:
        wstr (string): encoded string
        encoding (string): string encoding

    Returns:
        string: plain string
    """
    plain = ""
    for ch in wstr:
        byte = ch.encode(encoding)
        if len(byte) > 1:
            byte = (
                byte.replace(b"\\\\", b"\\")
                .replace(b'\\"', b'"')
                .replace(b"\\\n", b"\n")
            )
        plain = plain + byte.decode(encoding)
    return plain
