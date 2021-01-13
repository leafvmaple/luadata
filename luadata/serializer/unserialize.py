import math


def unserialize(s, encoding="utf-8", verbose=False):
    sbins = s.encode(encoding)
    root = {"entries": [], "lualen": 0, "is_root": True}
    node = root
    stack = []
    state = "START"
    pos = 0
    slen = len(sbins)
    byte_quoting_char = None
    key = None
    escaping = False
    errmsg = None

    def sorter(kv):
        if isinstance(kv[0], int):
            return kv[0]
        return math.inf

    def node_entries_append(node, key, val):
        node["entries"].append([key, val])
        node["entries"].sort(key=sorter)
        lualen = 0
        for kv in node["entries"]:
            if kv[0] == lualen + 1:
                lualen = lualen + 1
        node["lualen"] = lualen

    def node_to_table(node):
        if len(node["entries"]) == node["lualen"]:
            lst = []
            for kv in node["entries"]:
                lst.append(kv[1])
            return lst
        else:
            dct = {}
            for kv in node["entries"]:
                dct[kv[0]] = kv[1]
            return dct

    while pos <= slen:
        byte_current = None
        if pos < slen:
            byte_current = sbins[pos : pos + 1]
        if verbose:
            print("[step] pos", pos, byte_current, state, key, node)

        if state == "START":
            if byte_current is None:
                break
            if not node["is_root"] and (
                (byte_current >= b"A" and byte_current <= b"Z")
                or (byte_current >= b"a" and byte_current <= b"z")
                or byte_current == b"_"
            ):
                state = "KEY_SIMPLE"
                pos1 = pos
            elif not node["is_root"] and byte_current == b"[":
                state = "KEY_EXPRESSION_OPEN"
            elif byte_current == b"}":
                if len(stack) == 0:
                    errmsg = (
                        "unexpected table closing, no matching opening braces found."
                    )
                    break
                prev_env = stack.pop()
                if prev_env["state"] == "KEY_EXPRESSION_OPEN":
                    key = node_to_table(node)
                    state = "KEY_END"
                elif prev_env["state"] == "VALUE":
                    node_entries_append(
                        prev_env["node"],
                        prev_env["key"],
                        node_to_table(node),
                    )
                    state = "VALUE_END"
                    key = None
                node = prev_env["node"]
            elif (
                byte_current != b" "
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
            elif byte_current == b"t" and sbins[pos : pos + 4] == b"true":
                node_entries_append(node, key, True)
                state = "VALUE_END"
                key = None
                pos = pos + 3
            elif byte_current == b"f" and sbins[pos : pos + 5] == b"false":
                node_entries_append(node, key, False)
                state = "VALUE_END"
                key = None
                pos = pos + 4
            elif byte_current == b"{":
                stack.append({"node": node, "state": state, "key": key})
                state = "START"
                node = {"entries": [], "lualen": 0, "is_root": False}
        elif state == "VALUE_TEXT":
            if byte_current is None:
                errmsg = "unexpected string ending: missing close quote."
                break
            if escaping:
                escaping = False
            elif byte_current == b"\\":
                escaping = True
            elif byte_current == byte_quoting_char:
                node_entries_append(
                    node,
                    key,
                    sbins[pos1:pos]
                    .replace(b"\\\n", b"\n")
                    .replace(b'\\"', b'"')
                    .replace(b"\\\\", b"\\")
                    .decode(encoding),
                )
                state = "VALUE_END"
                key = None
        elif state == "VALUE_INT":
            if byte_current == b".":
                state = "VALUE_FLOAT"
            elif byte_current is None or byte_current < b"0" or byte_current > b"9":
                node_entries_append(
                    node,
                    key,
                    int(sbins[pos1:pos].decode(encoding)),
                )
                state = "VALUE_END"
                key = None
                pos = pos - 1
        elif state == "VALUE_FLOAT":
            if byte_current is None or byte_current < b"0" or byte_current > b"9":
                if pos == pos1 + 1 and sbins[pos1:pos] == b".":
                    errmsg = "unexpected dot."
                    break
                else:
                    node_entries_append(
                        node,
                        key,
                        float(sbins[pos1:pos].decode(encoding)),
                    )
                    state = "VALUE_END"
                    key = None
                    pos = pos - 1
        elif state == "VALUE_END":
            if byte_current is None:
                pass
            elif byte_current == b",":
                state = "START"
            elif byte_current == b"}":
                state = "START"
                pos = pos - 1
            elif (
                byte_current != b" "
                and byte_current != b"\t"
                and byte_current != b"\r"
                and byte_current != b"\n"
            ):
                errmsg = "unexpected character."
                break
        elif state == "KEY_EXPRESSION_OPEN":
            if byte_current is None:
                errmsg = "key expression expected."
                break
            if byte_current == b'"' or byte_current == b"'":
                state = "KEY_EXPRESSION_TEXT"
                pos1 = pos + 1
                byte_quoting_char = byte_current
            elif byte_current >= b"0" and byte_current <= b"9":
                state = "KEY_EXPRESSION_INT"
                pos1 = pos
            elif byte_current == b".":
                state = "KEY_EXPRESSION_FLOAT"
                pos1 = pos
            elif byte_current == b"t" and sbins[pos : pos + 4] == b"true":
                errmsg = "python do not support bool as dict key."
                break
                key = True
                state = "KEY_EXPRESSION_FINISH"
                pos = pos + 3
            elif byte_current == b"f" and sbins[pos : pos + 5] == b"false":
                errmsg = "python do not support bool variable as dict key."
                break
                key = False
                state = "KEY_EXPRESSION_FINISH"
                pos = pos + 4
            elif byte_current == b"{":
                errmsg = "python do not support lua table variable as dict key."
                break
                state = "START"
                stack.push({"node": node, "state": state, "key": key})
                node = {"entries": [], "lualen": 0}
        elif state == "KEY_EXPRESSION_TEXT":
            if byte_current is None:
                errmsg = "unexpected key expression string ending: missing close quote."
                break
            if escaping:
                escaping = False
            elif byte_current == b"\\":
                escaping = True
            elif byte_current == byte_quoting_char:
                key = (
                    sbins[pos1:pos]
                    .replace(b"\\\n", b"\n")
                    .replace(b'\\"', b'"')
                    .replace(b"\\\\", b"\\")
                    .decode(encoding)
                )
                state = "KEY_EXPRESSION_FINISH"
        elif state == "KEY_EXPRESSION_INT":
            if byte_current == b".":
                state = "KEY_EXPRESSION_FLOAT"
            elif byte_current is None or byte_current < b"0" or byte_current > b"9":
                key = int(sbins[pos1:pos].decode(encoding))
                state = "KEY_EXPRESSION_FINISH"
                pos = pos - 1
        elif state == "KEY_EXPRESSION_FLOAT":
            if byte_current is None or byte_current < b"0" or byte_current > b"9":
                if pos == pos1 + 1 and sbins[pos1:pos] == b".":
                    errmsg = "unexpected dot."
                    break
                else:
                    key = float(sbins[pos1:pos].decode(encoding))
                    state = "KEY_EXPRESSION_FINISH"
                    pos = pos - 1
        elif state == "KEY_EXPRESSION_FINISH":
            if byte_current is None:
                errmsg = 'unexpected end of table key expression, "]" expected.'
                break
            if byte_current == b"]":
                state = "KEY_EXPRESSION_CLOSE"
            elif (
                byte_current != b" "
                and byte_current != b"\t"
                and byte_current != b"\r"
                and byte_current != b"\n"
            ):
                errmsg = 'unexpected character, "]" expected.'
                break
        elif state == "KEY_EXPRESSION_CLOSE":
            if byte_current == b"=":
                state = "VALUE"
            elif (
                byte_current != b" "
                and byte_current != b"\t"
                and byte_current != b"\r"
                and byte_current != b"\n"
            ):
                errmsg = 'unexpected character, "=" expected.'
                break
        elif state == "KEY_SIMPLE":
            if not (
                (byte_current >= b"A" and byte_current <= b"Z")
                or (byte_current >= b"a" and byte_current <= b"z")
                or (byte_current >= b"0" and byte_current <= b"9")
                or byte_current == b"_"
            ):
                key = sbins[pos1:pos].decode(encoding)
                state = "KEY_SIMPLE_END"
                pos = pos - 1
        elif state == "KEY_SIMPLE_END":
            if (
                byte_current == b" "
                or byte_current == b"\r"
                or byte_current == b"\n"
                or byte_current == "\t"
            ):
                pass
            elif byte_current == b"=":
                state = "VALUE"
            elif byte_current == b"," or byte_current == b"}":
                if key == "true":
                    node_entries_append(node, node["lualen"] + 1, True)
                    state = "VALUE_END"
                    key = None
                    pos = pos - 1
                elif key == "false":
                    node_entries_append(node, node["lualen"] + 1, False)
                    state = "VALUE_END"
                    key = None
                    pos = pos - 1
                else:
                    key = None
                    errmsg = "invalied table simple key character."
                    break
        pos += 1
        if verbose:
            print("          ", pos, "    ", state, key, node)

    # check if there is any errors
    if errmsg is None and len(stack) != 0:
        errmsg = 'unexpected end of table, "}" expected.'
    if errmsg is None and root["lualen"] == 0:
        errmsg = "nothing can be unserialized from input string."
    if errmsg is not None:
        pos = min(pos, slen)
        start_pos = max(0, pos - 4)
        end_pos = min(pos + 10, slen)
        err_parts = sbins[start_pos:end_pos].decode(encoding)
        err_indent = " " * (pos - start_pos)
        raise Exception(
            "Unserialize luadata failed on pos %d:\n    %s\n    %s^\n    %s"
            % (pos, err_parts, err_indent, errmsg)
        )

    res = []
    for kv in root["entries"]:
        res.append(kv[1])
    return tuple(res)
