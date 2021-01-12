def __get_node_data(node):
    if node is None:
        return None
    if node["type"] == "string" or node["type"] == "int" or node["type"] == "float":
        return node["data"]
    if node["type"] == "table":
        d = {}
        for kv in node["entries"]:
            d[kv[0]] = kv[1]
        return d


def unserialize(s, encoding="utf-8"):
    sbins = s.encode(encoding)
    slen = len(sbins)
    root_node = None
    state = "START"
    pos = 0
    escaping = False
    errmsg = None
    while pos <= slen:
        byte_current = None
        if pos < slen:
            byte_current = sbins[pos : pos + 1]
        prev_state = state
        if state == "START":
            if byte_current is None:
                errmsg = "unexpected empty string."
                break
            if byte_current == b'"' or byte_current == b"'":
                state = "TEXT"
                pos1 = pos + 1
                byte_quoting_char = byte_current
            elif byte_current >= b"0" and byte_current <= b"9":
                state = "INT"
                pos1 = pos
            elif byte_current == b".":
                state = "FLOAT"
                pos1 = pos
        elif state == "TEXT":
            if byte_current is None:
                errmsg = "unexpected string ending: missing close quote."
                break
            if escaping:
                escaping = False
            elif byte_current == b"\\":
                escaping = True
            elif byte_current == byte_quoting_char:
                root_node = {
                    "type": "string",
                    "data": (
                        sbins[pos1:pos]
                        .replace(b"\\\n", b"\n")
                        .replace(b'\\"', b'"')
                        .replace(b"\\\\", b"\\")
                        .decode(encoding)
                    ),
                }
                state = "EOF"
        elif state == "INT":
            if byte_current == b".":
                state = "FLOAT"
            elif byte_current is None or byte_current < b"0" or byte_current > b"9":
                root_node = {
                    "type": "int",
                    "data": int(sbins[pos1:pos].decode(encoding)),
                }
                state = "EOF"
                pos = pos - 1
        elif state == "FLOAT":
            if byte_current is None or byte_current < b"0" or byte_current > b"9":
                if pos == pos1 + 1 and sbins[pos1:pos] == b".":
                    errmsg = "unexpected dot."
                    break
                else:
                    root_node = {
                        "type": "float",
                        "data": float(sbins[pos1:pos].decode(encoding)),
                    }
                    state = "EOF"
                    pos = pos - 1
        elif state == "EOF":
            if (
                byte_current is not None
                and byte_current != b" "
                and byte_current != b"\t"
                and byte_current != b"\r"
                and byte_current != b"\n"
            ):
                errmsg = "unexpected extra string."
                break
        pos += 1

    # check if there is any parsing errors
    if errmsg is not None:
        start_pos = max(0, pos - 4)
        end_pos = min(pos + 10, slen)
        err_parts = sbins[start_pos:end_pos].decode(encoding)
        err_indent = " " * (pos - start_pos)
        raise Exception(
            "Unserialize luadata failed on pos %d:\n    %s\n    %s^\n    %s"
            % (pos, err_parts, err_indent, errmsg)
        )

    return __get_node_data(root_node)
