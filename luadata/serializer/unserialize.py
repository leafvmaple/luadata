def unserialize(s, encoding="utf-8"):
    sbins = s.encode(encoding)
    root_node = {"entries": [], "lualen": 0}
    node = root_node
    stack = []
    state = "START"
    prev_state = None
    pos = 0
    slen = len(sbins)
    byte_quoting_char = None
    key = None
    escaping = False
    errmsg = None

    def node_append(node, key, val):
        if node["lualen"] + 1 == key:
            node["lualen"] = key
        node["entries"].append([key, val])

    while pos <= slen:
        byte_current = None
        if pos < slen:
            byte_current = sbins[pos : pos + 1]
        prev_state = state
        if state == "START":
            if (
                byte_current is not None
                and byte_current != b" "
                and byte_current != b"\t"
                and byte_current != b"\r"
                and byte_current != b"\n"
            ):
                key = node["lualen"] + 1
                state = "VALUE"
                pos = pos - 1
        elif state == "VALUE":
            if byte_current is None:
                errmsg = "unexpected empty value."
                break
            if byte_current == b'"' or byte_current == b"'":
                state = "VALUE_TEXT"
                pos1 = pos + 1
                byte_quoting_char = byte_current
            elif byte_current >= b"0" and byte_current <= b"9":
                state = "VALUE_INT"
                pos1 = pos
            elif byte_current == b".":
                state = "VALUE_FLOAT"
                pos1 = pos
        elif state == "VALUE_TEXT":
            if byte_current is None:
                errmsg = "unexpected string ending: missing close quote."
                break
            if escaping:
                escaping = False
            elif byte_current == b"\\":
                escaping = True
            elif byte_current == byte_quoting_char:
                node_append(
                    node,
                    key,
                    sbins[pos1:pos]
                    .replace(b"\\\n", b"\n")
                    .replace(b'\\"', b'"')
                    .replace(b"\\\\", b"\\")
                    .decode(encoding),
                )
                state = "VALUE_END"
        elif state == "VALUE_INT":
            if byte_current == b".":
                state = "VALUE_FLOAT"
            elif byte_current is None or byte_current < b"0" or byte_current > b"9":
                node_append(
                    node,
                    key,
                    int(sbins[pos1:pos].decode(encoding)),
                )
                state = "VALUE_END"
                pos = pos - 1
        elif state == "VALUE_FLOAT":
            if byte_current is None or byte_current < b"0" or byte_current > b"9":
                if pos == pos1 + 1 and sbins[pos1:pos] == b".":
                    errmsg = "unexpected dot."
                    break
                else:
                    node_append(
                        node,
                        key,
                        float(sbins[pos1:pos].decode(encoding)),
                    )
                    state = "VALUE_END"
                    pos = pos - 1
        elif state == "VALUE_END":
            if byte_current is None:
                pass
            elif byte_current == b",":
                state = "START"
            elif (
                byte_current != b" "
                and byte_current != b"\t"
                and byte_current != b"\r"
                and byte_current != b"\n"
            ):
                errmsg = "unexpected character."
                break
        pos += 1

    if errmsg is None and root_node["lualen"] == 0:
        errmsg = "unexpected empty string."
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

    res = []
    for kv in root_node["entries"]:
        res.append(kv[1])
    return tuple(res)
